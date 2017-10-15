# bottleneck

This application provides a debouncer for Status Webhooks heading
towards Discord. 

DAB Bot does not attempt to group its outgoing debug webhooks together,
leading to extreme ratelimits when all of a cluster's shards go down 
(such as during a Discord outage).

This project aims to provide as a middleman to help group webhooks
together.

### Configuration

The following values must be set in the configuration file prior to
running:

| key          | description                               |
| ------------ | ----------------------------------------- |
| `delay`      | Interval to process webhook queue         |
| `batch_size` | Number of Embeds to include per batch     |
| `url`        | Webhook URL                               |
| `token`      | Authorization header to validate requests |
| `host`       | Host to run Flask server on               |
| `port`       | Port to run Flask server on               |

### Usage

```http
POST /push HTTP/1.1
Host: <host>
Authorization: <auth token>
Content-Type: application/json

{
	"description": "embed content"
}
```