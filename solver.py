#!/usr/bin/python
# -*- coding: utf-8 -*-

from collections import namedtuple
import mixIntegerProgramming.facilityLocation_SCIP as facility_SCIP
import mixIntegerProgramming.facilityLocation_gurobi as facility_gurobi
import functions
import visualization

Point = namedtuple("Point", ['x', 'y'])
Facility = namedtuple("Facility", ['index', 'setup_cost', 'capacity', 'location'])
Customer = namedtuple("Customer", ['index', 'demand', 'location'])

def solve_it(input_data):
    # Modify this code to run your optimization algorithm

    # parse the input
    lines = input_data.split('\n')

    parts = lines[0].split()
    facility_count = int(parts[0])
    customer_count = int(parts[1])
    
    facilities = []
    for i in range(1, facility_count+1):
        parts = lines[i].split()
        facilities.append(Facility(i-1, float(parts[0]), int(parts[1]), Point(float(parts[2]), float(parts[3])) ))

    customers = []
    for i in range(facility_count+1, facility_count+1+customer_count):
        parts = lines[i].split()
        customers.append(Customer(i-1-facility_count, int(parts[0]), Point(float(parts[1]), float(parts[2]))))

    # build a solution
    option = input("(1) MIP: Gurobi Solver\n(2) MIP: SCIP Solver\n>>")
    solution = []
    if(option=="1"): solution = facility_gurobi.mip_facility_gurobi(facilities, customers)
    elif(option=="2"): solution = facility_SCIP.mip_facility_SCIP(facilities, customers)

    #validade_solution(solution, facilities, customers)
    
    if(visualization.__PLOT): visualization.plot(solution, facilities, customers)
        
    used = [0]*len(facilities)
    for facility_index in solution:
        used[facility_index] = 1

    # calculate the cost of the solution
    obj = sum([f.setup_cost*used[f.index] for f in facilities])
    for customer in customers:
        obj += functions.length(customer.location, facilities[solution[customer.index]].location)

    # prepare the solution in the specified output format
    output_data = '%.2f' % obj + ' ' + str(0) + '\n'
    output_data += ' '.join(map(str, solution))

    return output_data

def validade_solution(solution, facilities, customers):
    #validar demanda X capacidade
    capacity = [f.capacity for f in facilities]
    customer_index = 0
    for facility_index in solution:
        capacity[facility_index] -= customers[customer_index].demand
        #if(capacity[facility_index] < 0):  
           # print("The solution is invalid. The facility " + str(facility_index) + "can not deliver material to all customer assigned")
            #return False
        customer_index += 1
    
    print(capacity)
    
    
    
    return True

import sys

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        file_location = sys.argv[1].strip()
        with open(file_location, 'r') as input_data_file:
            input_data = input_data_file.read()
        print(solve_it(input_data))
    else:
        print('This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/fl_16_2)')

