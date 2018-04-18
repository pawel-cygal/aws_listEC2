import argparse
import boto.ec2
import sys
import ConfigParser
import os
import time


def list_ec2_instances(access_key,secret_key):
    regions = ['us-east-1','us-east-2','us-west-1','us-west-2','ca-central-1','eu-central-1',
               'eu-west-1','eu-west-2','ap-northeast-1','ap-southeast-1','ap-southeast-2' ]
    for region in regions:
        try:
            ec2_conn = boto.ec2.connect_to_region(region,
                aws_access_key_id=access_key,
                aws_secret_access_key=secret_key)
            reservations = ec2_conn.get_all_reservations()
            for reservation in reservations:
                for i in reservation.instances:
                    if i.state == 'running':
                        name = i.tags['Name'] if ('Name' in i.tags) else 'None'
                        timestamp = time.strftime('%Y%m%d-%H%M%S')
                        line = "Region: %s | InstanceID: %s | Type: %s | PrivateIP: %s | PublicIP: %s | Name: %s |" \
                        % (region, i.id, i.instance_type, i.private_ip_address, i.ip_address, name)
                        print line                       
                        f = open('ec2list-' + timestamp + '.txt', 'a')
                        f.write(line + '\n')
                        f.close
        except boto.exception.EC2ResponseError as err:
            print err
            print "========================"
            print "listec2.py -h for help" 
            sys.exit(1)

   
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--access-key', help='Access Key');
    parser.add_argument('--secret-access-key', help='Secret Access Key');
    args = parser.parse_args()
    access_key = args.access_key
    secret_key = args.secret_access_key
    
    if not access_key or not secret_key:
        try:
            print 'AWS credentials are not specified, fallback to ~/.aws/credentials'
            profile = os.environ.get('AWS_PROFILE', 'default')
            config = ConfigParser.ConfigParser()
            config.read([os.path.expanduser('~/.aws/credentials')])
            access_key = config.get(profile, 'aws_access_key_id')
            secret_access_key = config.get(profile, 'aws_secret_access_key')
        except IOError as err:
            print "File ~/.aws/credentials doesn't exist please create it or pass all required parameters from command line"
            sys.exit()
 
    print "Amazon Web Services: List of Running EC2 Instances:"
    list_ec2_instances(access_key, secret_key)


if  __name__ =='__main__':
    main()