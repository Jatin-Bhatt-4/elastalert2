# REFER TO INSTRUCTIONS.TXT FOR CONFIGURING ELASTALERT NOTIFICATION TO RINGCENTRAL GLIP

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
