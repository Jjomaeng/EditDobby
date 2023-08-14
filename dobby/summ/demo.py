import numpy as np
import os
import sys

import scipy.spatial
import matplotlib.pyplot as plt
from moviepy.editor import VideoFileClip, concatenate_videoclips



from config.settings import MEDIA_ROOT, BASE_DIR

def demo(video_name='Cosmus_Laundromat.mp4', summ_ratio=0.1):
    SUMM_RATIO = 0.1  # The maximum allowed ratio between the summary video and the full video.
    VIDEO_NAME = 'Cosmos_Laundromat.mp4'

    # Load data:
    print(BASE_DIR)
    print('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@'+os.path.join(BASE_DIR+'\\dobby\\summ\\data\\shots_features.npy'))
    X = np.load(os.path.join(BASE_DIR+'\\dobby\\summ\\data\\shots_features.npy'))  # Load n x d feature matrix. n - number of shots, d - feature dimension.
    C = np.load(os.path.join(BASE_DIR+'\\dobby\\summ\\data\\shots_durations.npy'))  # Load n x 1 shots duration array (number of frames per shot).

    # Calculate allowed budget
    budget = float(summ_ratio) * np.sum(C)

    # Use ILS_SUMM to obtain a representative subset which satisfies the knapsack constraint.
    representative_points, total_distance = ILS_SUMM(X, C, budget)

    # Display Results:
    representative_points = np.sort(representative_points)
    print("The selected shots are: " + str(representative_points))
    print("The achieved total distance is: " +str(np.round(total_distance,3)))
    u, s, vh = np.linalg.svd(X)
    plt.figure()
    point_size = np.divide(C, np.max(C)) * 100
    plt.scatter(u[:, 1], u[:, 2], s=point_size, c='lawngreen', marker='o')
    plt.scatter(u[representative_points, 1], u[representative_points, 2], s=point_size[representative_points],
                c='blue', marker='o')
    plt.title('Solution Visualization (total distance = ' + str(total_distance) + ')')
    plt.savefig(os.path.join(BASE_DIR+'\\dobby\\summ\\data\\Solution_Visualization'))

    # Generate the video summary file
    video_file_path = os.path.join(MEDIA_ROOT+'\\'+video_name)
    video_clip = VideoFileClip(video_file_path)
    shotIdx = np.concatenate(([0], np.cumsum(C[:-1])))
    frames_per_seconds = np.sum(C)/ video_clip.duration
    chosen_shots_clips = []
    for i in range(len(representative_points)):
        curr_start_time = shotIdx[representative_points[i]] / frames_per_seconds  # [Sec]
        if representative_points[i] == (shotIdx.__len__() - 1):
            curr_end_time = video_clip.duration
        else:
            curr_end_time = (shotIdx[representative_points[i] + 1] - 1) / frames_per_seconds  # [Sec]
        chosen_shots_clips.append(VideoFileClip(video_file_path).subclip(curr_start_time, curr_end_time))
    if chosen_shots_clips == []:
        print("The length of the shortest shots exceeds the allotted summarization time")
    else:
        summ_clip = concatenate_videoclips(chosen_shots_clips)

        summ_clip.write_videofile(os.path.join(MEDIA_ROOT+"\\summary\\"+video_name))


def demo_title(video_name, summ_ratio=0.01):
    SUMM_RATIO = 0.1  # The maximum allowed ratio between the summary video and the full video.
    VIDEO_NAME = 'Cosmos_Laundromat.mp4'

    # Load data:
    print(BASE_DIR)
    print('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@'+os.path.join(BASE_DIR+'\\dobby\\summ\\data\\shots_features.npy'))
    X = np.load(os.path.join(BASE_DIR+'\\dobby\\summ\\data\\shots_features.npy'))  # Load n x d feature matrix. n - number of shots, d - feature dimension.
    C = np.load(os.path.join(BASE_DIR+'\\dobby\\summ\\data\\shots_durations.npy'))  # Load n x 1 shots duration array (number of frames per shot).

    # Calculate allowed budget
    budget = float(summ_ratio) * np.sum(C)

    # Use ILS_SUMM to obtain a representative subset which satisfies the knapsack constraint.
    representative_points, total_distance = ILS_SUMM(X, C, budget)
    print(representative_points)
    # Display Results:
    representative_points = np.sort(representative_points)
    print("The selected shots are: " + str(representative_points))
    print("The achieved total distance is: " +str(np.round(total_distance,3)))
    u, s, vh = np.linalg.svd(X)
    plt.figure()
    point_size = np.divide(C, np.max(C)) * 100
    plt.scatter(u[:, 1], u[:, 2], s=point_size, c='lawngreen', marker='o')
    plt.scatter(u[representative_points, 1], u[representative_points, 2], s=point_size[representative_points],
                c='blue', marker='o')
    plt.title('Solution Visualization (total distance = ' + str(total_distance) + ')')
    plt.savefig(os.path.join(BASE_DIR+'\\dobby\\summ\\data\\Solution_Visualization'))

    # Generate the video summary file
    video_file_path = os.path.join(MEDIA_ROOT+'\\'+video_name)
    video_clip = VideoFileClip(video_file_path)
    shotIdx = np.concatenate(([0], np.cumsum(C[:-1])))
    frames_per_seconds = np.sum(C)/ video_clip.duration
    chosen_shots_clips = []
    for i in range(len(representative_points)):
        curr_start_time = shotIdx[representative_points[i]] / frames_per_seconds  # [Sec]
        if representative_points[i] == (shotIdx.__len__() - 1):
            curr_end_time = video_clip.duration
        else:
            curr_end_time = (shotIdx[representative_points[i] + 1] - 1) / frames_per_seconds  # [Sec]
        chosen_shots_clips.append(VideoFileClip(video_file_path).subclip(curr_start_time, curr_end_time))
    if chosen_shots_clips == []:
        print("The length of the shortest shots exceeds the allotted summarization time")
    else:
        summ_clip = concatenate_videoclips(chosen_shots_clips)

        summ_clip.write_videofile(os.path.join(MEDIA_ROOT+"\\title\\"+video_name))
        return representative_points
    return 

######################################################################################################



def ILS_SUMM(X, C, budget, ILS_max_trails=1):
    np.random.seed(100)
    distance_mat = scipy.spatial.distance_matrix(X, X)

    # Initialize the representative points:
    if np.min(C) > budget:
        print("The budget is less than the cheapest point!")
        return None
    else:
        curr_representative_points = [np.argmin(C)]

    # Local search for a local minimum:
    best_curr_representative_points, best_curr_total_distance = Local_Search(X, C, budget, initial_representative_points=curr_representative_points, distance_mat=distance_mat)

    # Initialize the best global point:
    best_global_representative_points = best_curr_representative_points
    best_global_total_distance = best_curr_total_distance

    MAX_M = 5
    for k in range(ILS_max_trails):
        M = 1
        while M <= MAX_M:
            # if k%10 == 0:
            print("ILS_SUMM - iteration number: " + str(k))
            print("Total distance: " + str(best_global_total_distance))
            # Perturb the best current point:
            curr_M = int(np.floor(np.min([len(best_curr_representative_points), M, len(C)-len(best_curr_representative_points)])))  # Ensure the size of permutation M is valid.
            exploration_representative_points = perturbation(X, C, budget, best_curr_representative_points, curr_M)
            # Local search for a local minimum, starting from the exploration point:
            best_exploration_representative_points, best_exploration_total_distance = Local_Search(X, C, budget, initial_representative_points=exploration_representative_points, distance_mat=distance_mat)
            # Decide which point will be the next curr point:
            best_curr_representative_points, best_curr_total_distance = acceptance_criterion(best_curr_representative_points, best_curr_total_distance, best_exploration_representative_points, best_exploration_total_distance)
            # Update the best global solution if a better point was found:
            if best_exploration_total_distance < best_global_total_distance:
                M = 1
                best_global_representative_points = best_exploration_representative_points
                best_global_total_distance = best_exploration_total_distance
            else:
                M += 1


    return best_global_representative_points, best_global_total_distance


def Local_Search(X, C, budget, initial_representative_points = None, distance_mat = None, Local_Search_max_trails=1000):
    np.random.seed(100)
    if distance_mat is None:
        distance_mat = scipy.spatial.distance_matrix(X, X)

    # Initialize the representative points:
    if initial_representative_points is not None:
        best_representative_points = initial_representative_points
    else:
        if np.min(C) > budget:
            print("The budget is less than the cheapest point!")
            return None
        else:
            best_representative_points = [np.argmin(C)]

    best_total_distance = calculate_total_distance(distance_mat, best_representative_points)

    for k in range(Local_Search_max_trails):
        if k % 10 == 0:
            print("Local Search - iteration number: " + str(k))
            print("Total distance: " + str(best_total_distance))
        best_rep_idx, best_point_idx, best_total_distance, IS_LOCAL_DISTANCE_IMPROVED = find_best_improvement_normalized_cost(X, C, budget, distance_mat, best_representative_points, best_total_distance)
        if IS_LOCAL_DISTANCE_IMPROVED == True:
            best_representative_points = update_representative_points(best_representative_points, best_point_idx,
                                                                    best_rep_idx)
        else:
            return best_representative_points, best_total_distance


    return best_representative_points, best_total_distance

def Restart_SUMM(X, C, budget, vid_duration, ILS_max_trails=1):
    np.random.seed(100)
    distance_mat = scipy.spatial.distance_matrix(X, X)

    # Initialize the representative points:
    if np.min(C) > budget:
        print("The budget is less than the cheapest point!")
        return None
    else:
        curr_representative_points = [np.argmin(C)]

    # Local search for a local minimum:
    best_curr_representative_points, best_curr_total_distance = Local_Search(X, C, budget, initial_representative_points=curr_representative_points, distance_mat=distance_mat)

    # Initialize the best global point:
    best_global_representative_points = best_curr_representative_points
    best_global_total_distance = best_curr_total_distance

    idxs = list(range(len(C)))
    permuted_idxs = list(np.random.permutation(idxs))
    for i in permuted_idxs:
        curr_representative_points = [i]
        if C[curr_representative_points] > budget:
            continue
        # Local search for a local minimum:
        best_curr_representative_points, best_curr_total_distance = Local_Search(X, C, budget,
                                                                                 initial_representative_points=curr_representative_points,
                                                                                 distance_mat=distance_mat)
        if best_curr_total_distance < best_global_total_distance:
            best_global_representative_points = best_curr_representative_points
            best_global_total_distance = best_curr_total_distance

    return best_global_representative_points, best_global_total_distance


def perturbation(X, C, budget, best_curr_representative_points, M):
    print("Perturbation with M = " + str(M))
    points_to_throw = np.argsort(-C[best_curr_representative_points])[0:(M)]

    # Build a list with all not medoids points:
    not_medoids_points = []
    for i in range(X.shape[0]):
        if i in best_curr_representative_points:
            pass
        else:
            not_medoids_points.append(i)
    not_medoids_points = np.array(not_medoids_points)

    # Build an array with the cheapest points.
    points_to_add_indices = np.argsort(C[not_medoids_points])[0:(M)]

    # Build a new solution of representative points by substituting costly points with cheap points.
    new_local_best_representative_points = np.copy(best_curr_representative_points)
    new_local_best_representative_points[points_to_throw] = not_medoids_points[points_to_add_indices]

    # Check that the new solution satisfies the budget condition:
    if np.sum(C[new_local_best_representative_points]) <= budget: # It is not necessary to happen because maybe the cheapest point that currently arn't medoids cost more then the current points.
        print("Perturbation is valid, M = " +str(M))
        local_best_representative_points = np.copy(new_local_best_representative_points)  # update to the new representative points
    else:
        local_best_representative_points = np.copy(best_curr_representative_points)  # stay with the original medoids.

    best_curr_representative_points = local_best_representative_points
    return best_curr_representative_points




def acceptance_criterion(best_curr_representative_points, best_curr_total_distance, best_exploration_representative_points, best_exploration_total_distance, criterion_type='Better'):
    if criterion_type == 'Better':
        if best_curr_total_distance < best_exploration_total_distance:
            return best_curr_representative_points, best_curr_total_distance
        else:
            return best_exploration_representative_points, best_exploration_total_distance
    elif criterion_type == 'RW':
        return best_exploration_representative_points, best_exploration_total_distance

    elif criterion_type == 'Metropolis':
        if np.random.binomial(1,0.5) == 1:
            best_exploration_representative_points, best_exploration_total_distance = acceptance_criterion(best_curr_representative_points, best_curr_total_distance,
                                 best_exploration_representative_points, best_exploration_total_distance,
                                 criterion_type='Better')
        else:
            best_exploration_representative_points, best_exploration_total_distance = acceptance_criterion(best_curr_representative_points, best_curr_total_distance,
                                 best_exploration_representative_points, best_exploration_total_distance,
                                 criterion_type='RW')
        return best_exploration_representative_points, best_exploration_total_distance





def calculate_total_distance(distance_mat, representative_points):
    effective_distance_mat = distance_mat[:,representative_points]
    distance_to_nearest_neighbor = np.min(effective_distance_mat,1)
    total_distance = np.sum(distance_to_nearest_neighbor)
    return total_distance


def update_representative_points(local_best_representative_points, best_point_idx, best_rep_idx):
    if best_rep_idx == None:
        current_k = local_best_representative_points.__len__()
        temp_local_best_representative_points = np.zeros(current_k + 1, dtype=int)
        temp_local_best_representative_points[:current_k] = local_best_representative_points
        temp_local_best_representative_points[current_k] = best_point_idx
        local_best_representative_points = np.copy(temp_local_best_representative_points)
    else:
        local_best_representative_points[int(np.where(local_best_representative_points == best_rep_idx)[0])] = best_point_idx
    return local_best_representative_points


def find_best_improvement_normalized_cost(X, C, budget, distance_mat, curr_representative_points, curr_total_distance):
    IS_LOCAL_DISTANCE_IMPROVED = False
    best_rep_idx = None
    best_point_idx = None
    curr_representative_points = np.array(curr_representative_points)
    near_points_data = get_near_points_data(distance_mat, curr_representative_points)
    local_best_total_distance = np.copy(curr_total_distance)
    # improvement_counter = 0

    for point_idx in range(X.shape[0]):
        if point_idx in curr_representative_points:
            continue
        if ((np.sum(C[curr_representative_points]) + C[point_idx]) <= budget):
            is_normalized_delta = False
            if is_normalized_delta == False:
                rep_idx = None # Don't replace a medoid but add one.
                delta_swap = get_delta_swap(distance_mat, near_points_data, rep_idx, point_idx)
                temp_total_distance = curr_total_distance + delta_swap
                if temp_total_distance < local_best_total_distance:
                    local_best_total_distance = temp_total_distance
                    best_rep_idx = rep_idx
                    best_point_idx = point_idx
                    IS_LOCAL_DISTANCE_IMPROVED = True
            else:
                best_normalized_delta_swap = 0
                rep_idx = None # Don't replace a medoid but add one.
                delta_swap = get_delta_swap(distance_mat, near_points_data, rep_idx, point_idx)
                delta_cost = C[point_idx]
                normalized_delta_swap = delta_swap / delta_cost
                if normalized_delta_swap < best_normalized_delta_swap:
                    temp_total_distance = curr_total_distance + delta_swap
                    local_best_total_distance = temp_total_distance
                    best_rep_idx = rep_idx
                    best_point_idx = point_idx
                    IS_LOCAL_DISTANCE_IMPROVED = True

    if IS_LOCAL_DISTANCE_IMPROVED == True:
        return best_rep_idx, best_point_idx, local_best_total_distance, IS_LOCAL_DISTANCE_IMPROVED
    else:
        for point_idx in range(X.shape[0]):
            if point_idx in curr_representative_points:
                continue
            for rep_idx in curr_representative_points:
                if (np.sum(C[curr_representative_points]) + C[point_idx] - C[rep_idx]) > budget:
                    continue
                delta_swap = get_delta_swap(distance_mat, near_points_data, rep_idx, point_idx, curr_representative_points)
                temp_total_distance = curr_total_distance + delta_swap
                if temp_total_distance < local_best_total_distance:
                    # If swapping the points decreases the total distance more then other options we checked:
                    # Keep it:
                    local_best_total_distance = temp_total_distance
                    best_rep_idx = rep_idx
                    best_point_idx = point_idx
                    IS_LOCAL_DISTANCE_IMPROVED = True
    return best_rep_idx, best_point_idx, local_best_total_distance, IS_LOCAL_DISTANCE_IMPROVED


def get_near_points_data(distance_mat, representative_points):
    # This function finds the nearest points to each point from the current representative points
    num_of_points = distance_mat.shape[0]
    points_idxs_list = range(num_of_points)
    near_points_data = np.zeros((num_of_points, 3))
    NEAREST_DIST = 0
    NEAREST_IDX = 1
    SECOND_DIST = 2
    # SECOND_IDX = 3
    argsorted_distance_to_rep_points = representative_points[np.argsort(distance_mat[:, representative_points], 1)]
    near_points_data[:, NEAREST_DIST] = distance_mat[tuple(points_idxs_list), tuple(argsorted_distance_to_rep_points[:,0])]
    near_points_data[:, NEAREST_IDX] = argsorted_distance_to_rep_points[:,0]
    if argsorted_distance_to_rep_points.shape[1] > 1:
        near_points_data[:, SECOND_DIST] = distance_mat[tuple(points_idxs_list), tuple(argsorted_distance_to_rep_points[:,1])]
    else:
        near_points_data[:, SECOND_DIST] = np.inf # No second nearest point
        # near_points_data[:, SECOND_IDX] = argsorted_distance_to_rep_points[:,1]
    return near_points_data


def get_delta_swap(distance_mat, near_points_data, original_med, candidate_median, curr_representative_points=None):
    NEAREST_DIST = 0
    NEAREST_IDX = 1
    SECOND_DIST = 2
    SECOND_IDX = 3
    num_of_points = near_points_data.shape[0]
    # points_idxs_list = range(num_of_points)
    delta_tot_dist = 0
    if original_med is None:
        delta_array = distance_mat[:, candidate_median] - near_points_data[:, NEAREST_DIST]
        delta_array_only_negetive = np.divide(delta_array - np.abs(delta_array), 2)
        delta_tot_dist = np.sum(delta_array_only_negetive)
    else:
        auxilary_mat = np.zeros((num_of_points,2))
        auxilary_mat[:, 0] = distance_mat[:, candidate_median] - near_points_data[:, NEAREST_DIST]  # d_oj - d_n
        auxilary_mat[:, 1] = near_points_data[:, SECOND_DIST] - near_points_data[:, NEAREST_DIST]  # d_s - d_n
        original_med_not_nearer_idxs = np.where(~(near_points_data[:, NEAREST_IDX] == original_med))
        auxilary_mat[original_med_not_nearer_idxs, 1] = 0
        delta_tot_dist = np.sum(np.min(auxilary_mat, 1))
    return delta_tot_dist








#####################################################################################################







if __name__ == "__main__":
    demo(sys.argv[1],float(sys.argv[2]))
