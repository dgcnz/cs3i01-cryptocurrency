# Proyecto Final

## Descripción

Una criptomoneda basica para probar los conceptos aprendidos de seguridad del curso Seguridad en Computacion. Cada instancia ejecutable es un nodo.

### Funcionalidad

- Hacer Proof of Work para confirmar transacciones.
- Hacer broadcasting de transaccion/bloque a otros nodos.

### Arquitectura

#### Multicontainer cliente-servidor

- Contenedor 1: Flask application (backend)
- Contenedor 2: Express application (frontend)
  - API documentation

#### Peer-to-peer network

- Networking using a REST API's using http protocol
- Hard-coded peers (for now)

#### Escalabillidad

- "Trilema de la escalabilidad" de blockchain
  - Escalabilidad
  - Seguridad
  - Descentralización
- Cada nodo independientemente puede escalar horizontal o verticalmente (Escalabilidad off-chain)

#### Características de seguridad - confiabilidad

- Integrity by proof of work hashes (SHA-256).
- Ed25519 signatures using NaCL
- Fixed proof of work difficulty
- Consistency and peer blockchain validation

#### Monitoreo

- Sentry cloud services
  - Logs usando python SDK

#### Tolerancia a fallas

- Excepciones
- Nodos independientes

#### Deployment

- Local: docker-compose set-up
  - network
- Remoto: aún no implementado :(

### Referencias

- [Blockchain Based Cloud Computing: Architecture and Research Challenges](https://ieeexplore.ieee.org/document/9252909/)
- [Containerizing Bitcoin and Ethereum with Docker](https://medium.com/mwpartners/containerizing-bitcoin-and-ethereum-with-docker-7c447b484f3a)

## Preguntas

### ¿Por qué escogió esa aplicación?

En el curso de Seguridad en Computacion estamos desarrollando un prototipo de criptomoneda y vimos que era una buena oportunidad para extender ese proyecto.

### ¿Qué características de la computación en nube pueden ser integradas en la aplicación?

- Contenerizacion y orquestramiento de contenedores.

## Resumen de los pasos necesarios para su ejecución

![](images/steps.png)
