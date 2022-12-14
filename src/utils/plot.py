import pandas as pd
import numpy as np
from pathlib import Path
from matplotlib import pyplot as plt
from typing import *


def plot(
    x: List[float],
    filepath: Path,
    xlabel: str = "",
    ylabel: str = "",
    hist: bool = False,
):
    if hist:
        fig, axes = plt.subplots(1, 2, figsize=(24, 8))
        axes[0].plot(x)
        axes[0].set_ylabel(ylabel)
        axes[0].set_xlabel(xlabel)

        axes[1].hist(x, bins=100)
        axes[0].set_xlabel(ylabel)
    else:
        fig, ax = plt.subplots(1, 1, figsize=(12, 8))
        ax.plot(x)
        ax.set_ylabel(ylabel)
        ax.set_xlabel(xlabel)
    fig.savefig(filepath)
    plt.close(fig)


def plot_from_baseline3(fromdir: Path, todir: Path):
    log = pd.read_csv(fromdir / "progress.csv")
    train_log = log.loc[~log["train/loss"].isnull()].reset_index(drop=True)
    eval_log = log.loc[~log["eval/mean_reward"].isnull()].reset_index(drop=True)

    plot(
        x=eval_log["eval/mean_reward"].values,
        filepath=todir / "eval_reward.png",
        xlabel="#eval",
        ylabel="eval reward",
    )

    plot(
        x=train_log["train/loss"].values,
        filepath=todir / "loss.png",
        xlabel="#eval",
        ylabel="loss",
    )


def eval_and_plot(model, market, savedir: Path):
    rewards = list()
    for i in range(market.num_steps):
        obs = market.state()
        action, _ = model.predict(obs)
        reward, _, _ = market.step(action=action)
        rewards.append(reward)

    result = market.get_return()
    result.to_csv(savedir / "result.csv")

    plot(
        x=result["rtn"].values,
        filepath=savedir / "return.png",
        xlabel="step",
        ylabel="return",
    )
    plot(
        x=result["cur_rtn"].values,
        filepath=savedir / "cur_return.png",
        xlabel="step",
        ylabel="cur return",
    )
    plot(
        x=np.cumsum(rewards),
        filepath=savedir / "reward.png",
        xlabel="step",
        ylabel="reward",
    )
