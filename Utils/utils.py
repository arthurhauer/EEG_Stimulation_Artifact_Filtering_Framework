from scipy import stats


def __generate_window_indexes(window_size: int, current_index: int):
    indexes = [0]*(2*window_size+1)
    indexes[window_size+1] = current_index
    for i in range(window_size):
        indexes[i] = current_index-window_size-i
        indexes[window_size+1+i] = current_index+i+1
    return indexes


def __get_window(window_size: int, samples: list, current_index: int) -> list:
    n_samples = len(samples)
    if(n_samples-current_index < window_size or current_index < window_size):
        raise Exception("Can't obtain window of size " +
                        str(window_size)+"from index "+str(current_index))
    window = [0]*(2*window_size+1)
    window[window_size+1] = samples[current_index]
    for i in range(window_size):
        window[i] = samples[current_index-window_size-i]
        window[window_size+i+1] = samples[current_index+i+1]
    return window

def first_order_differences(eeg: list) -> list:
    """
    Compute the differences between the current sample and the next one and sum through all channels.
    """
    n_samples = len(eeg[0])
    computed_diffs = [0]*n_samples
    for sample_index in range(n_samples):
        diff = 0
        for channel_index in range(len(eeg)):
            try:
                diff += eeg[channel_index][sample_index+1] - \
                    eeg[channel_index][sample_index]
            except:
                diff = 0
                break
        computed_diffs[sample_index] = diff
    return computed_diffs


def sliding_median_absolute_deviation(samples: list, window_size: int) -> list:
    """
    Compute the median absolute deviation based on a sliding window.
    """
    n_samples = len(samples)
    result = [0]*n_samples
    for t in range(n_samples):
        try:
            result[t] = stats.median_absolute_deviation(
                __get_window(window_size, samples, t))
        except:
            result[t] = 100
    return result
