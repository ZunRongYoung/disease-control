"""

Evaluate results

"""
import matplotlib.pyplot as plt
import collections
import argparse
import joblib
import os

from analysis import Evaluation, MultipleEvaluations

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--switch-backend", dest='plt_backend', type=str,
                        default="agg", help="Switch matplotlib backend")
    args = parser.parse_args()

    plt.switch_backend(args.plt_backend)

    saved = {
        0: 'test_all_Q_1_400_v2.pkl',
    }

    # select pickle files to import
    all_selected = [0]

    # FIXME: what is this?
    multi_summary_from_dump = False

    # summary for multi setting comparison
    multi_summary = collections.defaultdict(dict)
    if not multi_summary_from_dump:

        # Analyze each selected experiment
        for selected in all_selected:

            filename = saved[selected]
            expname = os.path.splitext(filename)[0]

            print(f"=== Analyzing experiment: {expname:s}")

            data = joblib.load(os.path.join('temp_pickles', filename))
            description = [d['name'] for d in data]
            dat = [d['dat'] for d in data]
            evaluation = Evaluation(dat, expname, description)

            multi_summary['Qs'][saved[selected]] = evaluation.data[0][0]['info']['Qx'][0]

            # Plot the experiment
            print("Make plots of the experiments:")
            evaluation.simulation_plot(
                process='X', filename='simulation_infection_summary',
                granularity=0.1, save=True)
            evaluation.simulation_plot(
                process='H', filename='simulation_treatment_summary',
                granularity=0.1, save=True)

            evaluation.infections_and_interventions_complete(save=True)
            evaluation.present_discounted_loss(plot=True, save=True)

            # Compute Comparison analysis data
            print("Compute comparison analysis data:")
            summary_tup = evaluation.summarize_interventions_and_intensities()

            summary_tup = evaluation.infections_and_interventions_complete(
                size_tup=(16, 10), save=True)

            # multi_summary['infections_and_interventions'][saved[selected]] = summary_tup
            # multi_summary['stats_intervention_intensities'][saved[selected]] = summary_tup

            # eval.debug()

        # dum = (saved, all_selected, multi_summary)
        # joblib.dump(dum, 'multi_comp_dump_{}'.format(saved[all_selected[-1]]))

    else:
        dum = joblib.load('multi_comp_dump_{}'.format(saved[all_selected[-1]]))
        saved = dum[0]
        all_selected = dum[1]
        multi_summary = dum[2]

    # Comparative analysis
    # multi_eval = MultipleEvaluations(saved, all_selected[-1], multi_summary)
    # multi_eval.compare_infections(size_tup=(5.0, 3.7), save=True)
