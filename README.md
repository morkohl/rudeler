# Rudeler

**This project is WIP. Code is subject to frequent change!**

Rudeler is an application that takes events from sources that publish airsoft events (f.e [Airsoft Verzeichnis](https://www.airsoft-verzeichnis.de/)) and publishes them to destinations (f.e [Spond](https://spond.com)). 

The application runs as a cloud function.

## Usage

### Installation

To clone and install a virtual environment:

```sh
git clone git@github.com:morkohl/rudeler.git
make venv
```


### Testing

> **In order to run integration tests you need a `.env.integrationtest` file.**
> 
> Find out what the content of this file should be in **[Credentials](#credentials)**.

#### Unit Tests

```sh
make unittest
```

#### Integration Tests

```sh
make integrationtest
```

#### All Tests

```sh
make test 
```

#### Coverage Report

Running a coverage report will run ALL tests.

```sh
make coverage-html
```

### Packaging & Deployment

#### Package code for Cloud Functions

```sh
make package environment=<environment>
```

#### Deploy

> **In order to deploy tests you need a file for your environment `.env.<environment>` file.**
>
> Find out what the content of this file should be in **[Credentials](#credentials)**.

```sh
make deploy environment=<environment>
```

The terraform variables can be found in **[variables.tf](terraform/variables.tf)**

## Credentials

Rudeler make targets will assume that you have a `.env` files for a few steps in order to supply credentials to the code running.

The name of this `.env` file for integration testing needs to be `.env.integrationtest` and for deployment `.env.<stage>`.

The content of this file should consist of all environment variables in **[config.py](src/rudeler/config.py)**.

