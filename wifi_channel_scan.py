import shlex
from subprocess import Popen, PIPE
from pathlib import Path
try:
    import matplotlib.pyplot as plt
except ImportError as e:
    plt = e


def _get_nmcli_device_scan_output():
    command = shlex.split('nmcli device wifi list')
    process = Popen(command, stdout=PIPE, stderr=PIPE)
    stdout, stderr = process.communicate()
    return stdout.decode()


def _create_channel_map(ch_list):
    map_dict = {}
    for c in ch_list:
        map_dict[c] = map_dict.get(c, 0) + 1
    return map_dict


def find_used_channels():
    band_2_4 = []
    band_5 = []
    nmcli_device_wifi_list = _get_nmcli_device_scan_output()
    for r in nmcli_device_wifi_list.split("\n"):
        if r.startswith("IN"):
            continue
        row = r.split()
        for c in row:
            try:
                channel = int(c)
                list_to_store = band_2_4 if channel < 12 else band_5
                list_to_store.append(channel)
                break
            except ValueError:
                continue
    result_map = {}
    for b, channels in zip(("Band 2.4 GHz", "Band 5 GHz"), (band_2_4, band_5)):
        result_map[b] = _create_channel_map(channels)
    return result_map


def find_least_crowded(map_dict):
    order_list = sorted(map_dict, key=map_dict.get)
    for item in order_list:
        print(f"Channel: {item} --> number of networks: {map_dict[item]}")


def plot_results(data):
    fig = plt.figure(figsize=(9, 6))
    axes = fig.subplots(2, 1)

    for i, key in enumerate(data):
        sorted_channels = sorted(data[key])
        values = [data[key][k] for k in sorted_channels]

        axes[i].scatter(range(len(sorted_channels)), values, color='red', s=50)

        axes[i].set_ylabel("Number of networks")
        axes[i].set_title(key)

        plt.setp(axes[i], xticks=range(len(sorted_channels)), xticklabels=[f"Channel [{channel}]" for channel in sorted_channels])
        plt.setp(axes[i], yticks=range(max(values) + 1))

    plt.tight_layout()
    fp = Path(Path.cwd(), "channel_plot.pdf")
    fig.savefig(fp)
    plt.close(fig)


def run():
    res = find_used_channels()
    print("<<<< 2.4 GHz >>>>")
    find_least_crowded(res["Band 2.4 GHz"])
    print("-" * 35)
    print("<<<< 5 GHz >>>>")
    find_least_crowded(res["Band 5 GHz"])
    print("-" * 35)
    if not isinstance(plt, ImportError):
        plot_results(res)


if __name__ == "__main__":
    run()
