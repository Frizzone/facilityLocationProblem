
from ortools.linear_solver import pywraplp
import functions
from datetime import datetime


def mip_facility_SCIP(facilities, customers):
    # Create the mip solver with the SCIP backend.
    solver = pywraplp.Solver.CreateSolver('SCIP')
    
    #create variables A e F
    # Afc = 1 -> cliente c é atendido por facility f
    # Ff = 1 -> facility f esta aberta
    A = [[0 for x in range(len(facilities))] for y in range(len(customers))]
    F = [0 for x in range(len(facilities))]
    for facility in facilities:
        F[facility.index] = solver.BoolVar(str(facility.index))
        for customer in customers:
            A[customer.index][facility.index] = solver.BoolVar(str(customer.index)+","+str(facility.index))
    
    #/print('Number of variables =', solver.NumVariables())
    
    # Add constraint: um cliente é atendido por apenas 1 local
    for customer in customers:
        solver.Add(sum([A[customer.index][f.index] for f in facilities]) == 1)
        
    # Add constraint: a demanda dos clientes pode ser atendida pela capacidade do local
    for facility in facilities:
        solver.Add(sum([c.demand * A[c.index][facility.index] for c in customers]) <= facility.capacity)


    # Add constraint: para dar valores corretos variável F
    for facility in facilities:
        solver.Add(sum([A[c.index][facility.index] for c in customers]) <= len(customers) * F[facility.index])
            
    
    # Set objective
    solver.Minimize(sum([F[f.index] * f.setup_cost for f in facilities]) + sum([sum([A[c.index][f.index] * functions.length(f.location, c.location) for f in facilities]) for c in customers]))

    solver.SetTimeLimit(1000*60*120) #60 minutes
    gap = 0.05
    solverParams = pywraplp.MPSolverParameters()
    solverParams.SetDoubleParam(solverParams.RELATIVE_MIP_GAP, gap)    

    #print(solver.ExportModelAsMpsFormat(True, True))

    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL or pywraplp.Solver.FEASIBLE:
        #print('Time = ', solver.WallTime(), ' milliseconds')
        solution = [-1]*len(customers)
        for customer in customers:
            for facility in facilities:
                if(A[customer.index][facility.index].solution_value() == 1):
                    if(solution[customer.index] != -1):
                        print('The solutions has more than one facility to the same customer.')
                        break;
                    else: solution[customer.index] = facility.index
        
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        print('\nAdvanced usage:')
        print("Current Time =", current_time)
        print('Problem solved in %f milliseconds' % solver.wall_time())
        print('Problem solved in %d iterations' % solver.iterations())
        print('Problem solved in %d branch-and-bound nodes' % solver.nodes())
        return solution
    else:
        print('The problem does not have an optimal solution.')
