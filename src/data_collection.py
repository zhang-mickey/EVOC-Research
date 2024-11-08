from revolve2.modular_robot import ModularRobot
from revolve2.modular_robot.brain.cpg import BrainCpgNetworkStatic

import pandas as pd
import numpy as np
import config

from typedef import simulated_behavior

def record_cpg(robot: ModularRobot, run_id: int):
    filename = config.best_solution_per_ea
    brain: BrainCpgNetworkStatic = robot.brain
    pd.DataFrame(np.array(brain._weight_matrix)).to_csv(f"best-cpg-gen-{run_id}.csv", index=False, header=False)
    # return NotImplementedError()

def record_behavior(robot: ModularRobot, fitness: float, behavior: simulated_behavior, generation_id: int = -1):
    # HACK: Type here is body but expects BodyV2. The type match is guarenteed
    #       because we use `gecko_v2` to construct the body, which uses the
    #       BodyV2 subtype. 
    csv_map = config.body_to_csv_map(robot.body) 


    for idx, state in enumerate(behavior):
        pose_func = state.get_modular_robot_simulation_state(robot).get_module_absolute_pose
        
        robot_coord_list = []
        
        def col_map(col: str):
            match col:
                case "generation_id": return generation_id
                case "center-euclidian": return 0 # calculate this after
                case "generation_best_fitness_score": return fitness
                case "frame_id": return idx
                case _:
                    abs_pose = pose_func(csv_map[col])
                    robot_coord_list.append((abs_pose.position.x, abs_pose.position.y))
                    return f"({abs_pose.position.x},{abs_pose.position.y})"
        
        # Collect the robots coordinates and put it in a dictionary that matches
        # the CSV definition `csv_cols`
        row = {col: col_map(col) for col in config.csv_cols}
        
        pd_coord_list = pd.DataFrame(robot_coord_list, columns=['x', 'y'])
        row["center-euclidian"] = f"({pd_coord_list['x'].mean()},{pd_coord_list['y'].mean()})"
        
        config.write_buffer.loc[len(config.write_buffer.index)] = row
    
    
