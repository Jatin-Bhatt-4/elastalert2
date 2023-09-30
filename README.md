# ElastAlert 2

ElastAlert 2 is a standalone software tool for alerting on anomalies, spikes, or other patterns of interest from data in [Elasticsearch][10] and [OpenSearch][9].

ElastAlert 2 is backwards compatible with the original [ElastAlert][0] rules.

![CI Workflow](https://github.com/jertel/elastalert/workflows/master_build_test/badge.svg)

## Docker and Kubernetes

ElastAlert 2 is well-suited to being run as a microservice, and is available
as an image on [Docker Hub][2] and on [GitHub Container Registry][11]. For more instructions on how to
configure and run ElastAlert 2 using Docker, see [here][8].

A [Helm chart][7] is also included for easy configuration as a Kubernetes deployment. 

## Documentation

Documentation, including an FAQ, for ElastAlert 2 can be found on [readthedocs.com][3]. This is the place to start if you're not familiar with ElastAlert 2 at all.

Elasticsearch 8 support is documented in the [FAQ][12].

The full list of platforms that ElastAlert 2 can fire alerts into can be found [in the documentation][4].

## Contributing

Please see our [contributing guidelines][6].

## License

ElastAlert 2 is licensed under the [Apache License, Version 2.0][5].

[0]: https://github.com/yelp/elastalert
[1]: https://github.com/jertel/elastalert2/blob/master/examples/config.yaml.example
[2]: https://hub.docker.com/r/jertel/elastalert2
[3]: https://elastalert2.readthedocs.io/
[4]: https://elastalert2.readthedocs.io/en/latest/ruletypes.html#alerts
[5]: https://www.apache.org/licenses/LICENSE-2.0
[6]: https://github.com/jertel/elastalert2/blob/master/CONTRIBUTING.md
[7]: https://github.com/jertel/elastalert2/tree/master/chart/elastalert2
[8]: https://elastalert2.readthedocs.io/en/latest/running_elastalert.html
[9]: https://opensearch.org/
[10]: https://github.com/elastic/elasticsearch
[11]: https://github.com/jertel/elastalert2/pkgs/container/elastalert2%2Felastalert2
[12]: https://elastalert2.readthedocs.io/en/latest/recipes/faq.html#does-elastalert-2-support-elasticsearch-8

**************************************************************************************************************************************************************************************************************

The purpose of this project is to send Elastalert from Elasticsearch to RingCentral Glip.

To get the webhook URL , Create a team group in RingCentral & configure Incoming Webhook using Add Apps option. Copy the webhook URL to use in rc_glip.yaml(Rule file) 

Once you have installed & configured elastalert in your server follow the below steps:-

1. Create a file to start/stop elastalert service at path /etc/init.d/elastalert

#!/bin/bash
# elastalert   startup script for elastalert
# pidfile:           /var/run/elastalert.pid
# chkconfig: 2345 99 01

NAME=elastalert
PIDFILE=/var/run/$NAME.pid
ELASTALERT_DIR=/etc/elastalert
ELASTALERT_USER=root
CONFIG_FILE=/etc/elastalert/config.yml
ELASTALERT=/root/myenv/bin/elastalert #Change the path according to your configuration(I have used this as I am running elastalert in python virtual environment)

. /etc/rc.d/init.d/functions

case $1 in
   start)
      echo -n $"Starting $NAME: "
      cd $ELASTALERT_DIR
      daemon --user="$ELASTALERT_USER" --pidfile="$PIDFILE" "$ELASTALERT --config $CONFIG_FILE &"
      RETVAL=$?
      pid=`ps -ef | grep python | grep elastalert | awk '{print $2}'`
      if [ -n "$pid" ]; then
        echo $pid > "$PIDFILE"
      fi
   ;;
   stop)
      echo -n $"Stopping $NAME: "
      killproc -p "$PIDFILE" -d 10 "$ELASTALERT"
      RETVAL="$?"
      echo
      [ $RETVAL = 0 ] && rm -f "$PIDFILE"
   ;;
   *)
      echo "Usage: /etc/init.d/elastalert {start|stop}" ;;
esac
exit 0

**************************************************************************************************************************************************************************************************************

2. Now create config.yml at /etc/elastalert/config.yml with rules folder path & your elasticsearch domain

# This is the folder that contains the rule yaml files
# Any .yaml file will be loaded as a rule
rules_folder: rules
scan_subdirectories: true
# How often ElastAlert will query Elasticsearch
# The unit can be anything from weeks to seconds
run_every:
  minutes: 5

# ElastAlert will buffer results from the most recent
# period of time, in case some log sources are not in real time
buffer_time:
  minutes: 20

# The Elasticsearch hostname for metadata writeback
# Note that every rule can have its own Elasticsearch host
es_host: your.elasticsearch.domain

# The Elasticsearch port
es_port: 9200

# The AWS region to use. Set this when using AWS-managed elasticsearch
#aws_region: us-east-1

# The AWS profile to use. Use this if you are using an aws-cli profile.
# See http://docs.aws.amazon.com/cli/latest/userguide/cli-chap-getting-started.html
# for details
profile: default

# Optional URL prefix for Elasticsearch
es_url_prefix: ''

# Connect with TLS to Elasticsearch
use_ssl: false

# Verify TLS certificates
#verify_certs: True

# GET request with body is the default option for Elasticsearch.
# If it fails for some reason, you can pass 'GET', 'POST' or 'source'.
# See http://elasticsearch-py.readthedocs.io/en/master/connection.html?highlight=send_get_body_as#transport
# for details
es_send_get_body_as: GET

# Option basic-auth username and password for Elasticsearch
#es_username: someusername
#es_password: somepassword

# The index on es_host which is used for metadata storage
# This can be a unmapped index, but it is recommended that you run
# elastalert-create-index to set a mapping
writeback_index: elastalert_status
es_conn_timeout: 30

# If an alert fails for some reason, ElastAlert will retry
# sending the alert until this time period has elapsed
alert_time_limit:
  days: 2

**************************************************************************************************************************************************************************************************************

3. Create a rules folder inside which your rules will be placed(/etc/elastalert/rules) & create another folder with name elastalert_modules as /etc/elastalert/elastalert_modules

4. At /etc/elastalert/elastalert_modules , place glip.py file provided in the elastalert folder.

5. At /etc/elastalert/rules , place rc_glip.yaml file provided in elastalert folder.

6. Restart the elastalert service using commands-
   /etc/init.d/elastalert stop
   /etc/init.d/elastalert start

7. When the event occurs , you will get notification in elastalert glip like you receive email for same elastalert.


