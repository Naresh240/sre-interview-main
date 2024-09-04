# FastAPI Inventory Management Application

This repository contains a simple FastAPI application for managing an inventory of items. The application exposes RESTful endpoints and integrates with Prometheus for monitoring metrics.

## Tasks

### 1. Make the Application Run as Expected
- Ensure the FastAPI application starts without errors.
- Verify that all defined endpoints are functional.

### 2. Add validation of positive quantity
- Product quantity in create / update must be positive number
- When updating the product the updated quantity is the current quantity

### 3. Implement the `/metrics` Endpoint
- The application should expose a `/metrics` endpoint that provides Prometheus metrics for monitoring.

### 4. Add a Metric for Current Product Quantity
- Implement a metric that shows the current quantity of each product in the inventory.
- This metric should use `product_name` as a label.

### 5. Add Alertmanager to the Project
- Set up Alertmanager to monitor specific conditions:
  - **Item Quantity Close to 0**: Trigger an alert if any item's quantity is 2 or below.
  - **Sudden Drop in Item Quantity**: Trigger an alert if an item's quantity drops significantly (e.g., from 15 to 7).

### 6. Add SLO alerts for app latency & error rate
- Api latency is above 10ms (Implement additional metrics if needed) & error rate is 99.95%
- Group / supress overlapping alerts

### 7. Add All Relevant Components to Docker Compose
- Update the `docker-compose.yml` file to include the Alertmanager service.
- Ensure that all components (FastAPI, Prometheus, Alertmanager) are properly configured and can communicate with each other.

### 8. 

## Bonus Task

### 1. Migrate from Pip to Poetry
- Convert the project dependencies from using `pip` and `requirements.txt` to using `Poetry`.
- Ensure that the project can still run smoothly with the new dependency management system.

### 2. Add unit tests
- Add functional unit testing
- Add coverage testing

## Requirements

- Once all tasks are completed, open a Pull Request (PR) with your changes.

## Solutions:

1. Run below commands to run application:

```bash
docker-compose build --no-cache
docker-compose up -d
```

2. Check Output using below urls:

```bash
curl -X POST "http://54.166.15.182:8000/items/" -H "Content-Type: application/json" -d '{"name": "item1", "price": 10.0, "quantity": 5, "description": "A test item"}'
curl -X GET "http://54.166.15.182:8000/items/item1"

```

3. Access metrics API:

   http://<PublicIP>:8000/metrics
   
4. Access prometheous:

    http://<PublicIP>:9090/

5. Access Alert Manager:
     http://<PublicIP>:9093/
