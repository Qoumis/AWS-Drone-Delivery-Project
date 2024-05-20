# AWS-Drone-Delivery-Project
Event-driven serverless application, developed by using Amazon Web Services (AWS) Educational Starter account, as a part of Academic course CS - 452 .

### Case Study: Drone Delivery: An efficient way to reduce delivery time and traffic congestion
#### Brief description

This project aims to develop an efficient drone delivery service system involving retailers, drone delivery providers, and clients. 
Clients request last-mile delivery services from providers with a limited number of drones. We aim to create a scheduling algorithm to efficiently serve these requests. 
Time is divided into rounds, with a fixed number of requests received at the start of each round. 
An auction determines which requests are fulfilled and at what cost, with unfulfilled requests carried over to the next round.

#### The service system consists of the following entities:
##### 1. Product retailer:
   - Manages service requests
   - Pricing Policy
   - Decision: Which requests to serve
   - Selection criteria: Bids
   - Goal: efficiency (total sum of clients utility is maximized)
##### 2. Drone delivery provider:
   - Intermediate that undertakes the delivery of the product
   - Decision: what is the delivery order of the winning requests
   - Goal: efficiency (total time is minimized)
##### 3. Clients:
   - People buying products/services on the retailer’s website
   - Decision: what bid to submit

#
#### A Petri net that represents the drone delivery service system for two consecutive bidding rounds, that includes 2 drones and 4 customers.
![Screenshot from 2024-05-20 15-51-39](https://github.com/Qoumis/AWS-Drone-Delivery-Project/assets/85035805/e46db47c-ac1c-4b01-8664-42a7db1d3d4b)

#
#### The final implementation utilizing serverless technologies is illustrated in the figure below:
![Screenshot from 2024-05-20 16-05-40](https://github.com/Qoumis/AWS-Drone-Delivery-Project/assets/85035805/bd5de8df-98d8-4e5d-a14d-52845e986ed8)

#
##### For more information regarding the assignment and the final implementation you can check out the project's promt and the report.pdf
