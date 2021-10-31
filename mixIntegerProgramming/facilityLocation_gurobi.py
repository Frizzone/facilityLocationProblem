import gurobipy as gp 
from gurobipy import *
import functions

def mip_facility_gurobi(facilities, customers):
    try:
        # Create a new model
        m = gp.Model("facility")

        # Create variables 
        #A[c][f] = 1 then Facility f is assign to customer c
        #F[f] = 1 the facility f is opened, that means, is assign to at least one customer.
        A = [[-1 for x in range(len(facilities))] for y in range(len(customers))]
        F = [0 for x in range(len(facilities))]
        for facility in facilities:
            F[facility.index] = m.addVar(vtype=GRB.BINARY, name=str(facility.index))
            for customer in customers:
                A[customer.index][facility.index] = m.addVar(vtype=GRB.BINARY, name=str(customer.index)+","+str(facility.index))

        # Add constraint: a customer is assigned to one facility
        for customer in customers:
            m.addConstr(sum([A[customer.index][f.index] for f in facilities]) == 1, "c"+str(customer.index))

        # Add constraint: the total demand of customers assign to one facility is less or equal the facility capacity
        for facility in facilities:
            m.addConstr(sum([c.demand * A[c.index][facility.index] for c in customers]) <= facility.capacity, "d"+str(facility.index))

        # Add constraint: para dar valores corretos variável F
        for facility in facilities:
            m.addConstr(sum([A[c.index][facility.index] for c in customers]) <= len(customers) * F[facility.index], "f"+str(facility.index))
            

        # Set objective: minimize the total set_cost (per opened facility) + the cost of transportation between the facilities and customres associated.
        m.setObjective(sum([F[f.index] * f.setup_cost for f in facilities]) + sum([sum([A[c.index][f.index] * functions.length(f.location, c.location) for f in facilities]) for c in customers]), GRB.MINIMIZE)

   
        #m.write('model.lp')
        
        #parameters: time limit and gap
        m.Params.TimeLimit =60*10
        #m.Params.MIPGap=0.1
    
        # Optimize model
        m.optimize()

        #process the solution output
        S = [[-1 for x in range(len(facilities))] for y in range(len(customers))]
        for v in m.getVars():
            indexs = v.varName.split(",")
            if(len(indexs)>1):
                S[int(indexs[0])][int(indexs[1])] = int(v.x)
                
        solution = [-1]*len(customers)
        for customer in customers:
            for facility in facilities:
                if(S[customer.index][facility.index] == 1):
                    if(solution[customer.index] != -1):
                        print('The solutions has more than one facility to the same customer.')
                        break;
                    else: solution[customer.index] = facility.index
                    
        return solution
        print('Obj: %g' % m.objVal)

    except gp.GurobiError as e:
        print('Error code ' + str(e.errno) + ': ' + str(e))
