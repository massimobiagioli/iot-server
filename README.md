# IoT Server

This is a FastAPI-based IoT server that manages device connections and data through MQTT messaging. The server provides a web interface for monitoring connected devices and handles real-time device status updates.

## Features

- **Device Management**: Track and monitor IoT devices with real-time status updates
- **MQTT Integration**: Handle device messages through MQTT protocol
- **Web Interface**: Modern responsive web UI for device monitoring
- **Database Storage**: SQLite database with Prisma ORM for data persistence
- **Real-time Updates**: Live device connection status tracking

## Requirements

- Python 3.8+
- SQLite database
- MQTT broker (for device communication)

## Installation

Install all project dependencies:

```bash
make install
```

This command will upgrade pip and install all required packages from `requirements_dev.txt`.

## Database Setup

Generate the Prisma client:

```bash
make prisma-generate
```

Push the database schema:

```bash
make prisma-db-push
```

For specific environments, use:

```bash
make prisma-db-push stage=test
```

## Development

### Running the Server

Start the development server:

```bash
make server
```

Or specify a custom port:

```bash
make server port=8080
```

The server will start with auto-reload enabled for development.

### Code Quality

**Linting**: Check code style and potential issues:

```bash
make lint
```

**Auto-fix linting issues**:

```bash
make lint-fix
```

**Format code**:

```bash
make format
```

### Testing

**Run all tests**:

```bash
make test
```

**Run specific tests**:

```bash
make test filter=tests/test_devices.py
```

**Run tests with coverage report**:

```bash
make coverage
```

## Project Structure

The project follows a Command/Query pattern architecture:

- `src/`: Main application source code
- `tests/`: Test files
- `prisma/`: Database schema and migrations
- `templates/`: Jinja2 HTML templates
- `static/`: Static web assets

## Device Management

The server handles device status messages through MQTT queues:

- **Device Registration**: Automatically creates new devices when they connect
- **Status Updates**: Tracks connection/disconnection events
- **Device Information**: Stores device type, name, and last seen timestamp

Message format:
```json
{
  "payload": {
    "device_type": "esp32",
    "device_id": "0c4f5500",
    "device_name": "tester"
  },
  "timestamp": 806226802,
  "event_type": "connected"
}
```

## Deploy

For deployment instructions, see [deploy.md](deploy.md).

## Help

To see all available commands:

```bash
make help
```

This will display all Makefile targets with their descriptions.