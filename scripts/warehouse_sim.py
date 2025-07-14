# simulation script 

# import the required libraries
import simpy
import random
import pandas as pd

# random seed for reproducibility
random.seed(42)

Order_interval = [1, 3]   # Minutes betweeen order arrivals (random)
num_workers = 3           # number of packers (resources)
packing_time = [3, 8]     # minutes to process order
sim_time = 8 * 60         # simlulating 8 hours (in minutes)


order_log = []



# Defining the order fullfilment process

def Order_process(env, order_id, warehouse):
    """simulate the time takes to process one order"""
    arrival_time = env.now

    
    with warehouse.request() as request:     #request a worker
        yield request                        # wait until a worker is available
        waiting_time = env.now - arrival_time
        
        #print(f'Order {order_id} waited {waiting_time:.2f} minutes')
        
        service_time = random.uniform(*packing_time)   # simulate the packing time
        yield env.timeout(service_time)
        finish_time = env.now

        #print(f'Order {order_id} processed in {service_time:.2f} minutes')

        #loging the order simulation 
        order_log.append({
            'order_id' : order_id,
            'arrival_time' : arrival_time,
            'waiting_time' : waiting_time,
            'service_time' : service_time,
            'finish_time' : finish_time

        })



# Define the order generator

def Order_generator(env, warehouse):
    """Generates orders at random intervals and send them to be processed"""
    order_id = 0
    while True:
        yield env.timeout(random.uniform(*Order_interval))
        order_id += 1
        env.process(Order_process(env, order_id, warehouse))


# Run the simulation 

def Run_simulation():
    print('Starting Simulation ...')

    # Initialize the Environment and resources
    env = simpy.Environment()
    warehouse = simpy.Resource(env, capacity=num_workers)

    # Start the order generator
    env.process(Order_generator(env, warehouse))

    #run the simulation
    env.run(until=sim_time)
    
    print('Simulation Completed ...')


if __name__ == '__main__':
    Run_simulation()


df = pd.DataFrame(order_log)
df.to_csv("warehouse-simulation-logistics/data/processed/order_log.csv", index=False)


print("/n saved simulation results to data/processed/order_log.csv")
