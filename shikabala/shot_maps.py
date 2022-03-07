from typing import Tuple
import statsbomb as sb
import pandas as pd


from mplsoccer import VerticalPitch


def get_event(event_id: str) -> object:
    events = sb.Events(event_id=event_id)
    return events


def get_df_for_event(event_id: str) -> pd.DataFrame:
    events = get_event(event_id)
    df = events.get_dataframe(event_type="shot")
    return df


def split_df(
    event_id: str, team_1: str, team_2: str
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    df = get_df_for_event(event_id)
    team_1_df = df[df["team"] == team_1].copy()
    team_2_df = df[df["team"] == team_2].copy()
    return team_1_df, team_2_df


def split_df_goals(df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]:
    goal_df = df[df["outcome"] == "Goal"].copy()
    non_goal_df = df[df["outcome"] != "Goal"].copy()
    return goal_df, non_goal_df


def create_vertical_pitch(half: bool, v_size: int, h_size: int):
    pitch = VerticalPitch(half=half)
    fig, ax = pitch.draw(figsize=(v_size, h_size))
    return fig, ax, pitch


def create_scatter_plot_event(
    event_id: str, half: bool, v_size: int, h_size: int, color: str
):
    df = get_df_for_event(event_id)
    fig, ax, pitch = create_vertical_pitch(half, v_size, h_size)
    sc = pitch.scatter(  # noqa: F841
        df["start_location_x"],
        df["start_location_y"],
        s=df["statsbomb_xg"] * 500 + 100,
        cmap=color,
        c=df["statsbomb_xg"],
        ax=ax,
    )


def create_scatter_plot_for_one_team(
    team_df: pd.DataFrame, color: str, team_label, pitch, ax, marker=None
):
    sc = pitch.scatter(  # noqa: F841
        team_df["start_location_x"],
        team_df["start_location_y"],
        s=team_df["statsbomb_xg"] * 500 + 100,
        c=color,
        hatch="//",
        ax=ax,
        label=team_label,
        marker=marker,
    )  # noqa: F841


def create_scatter_plot_for_two_teams(
    event_id: str,
    half: bool,
    v_size: int,
    h_size: int,
    color_1: str,
    color_2: str,
    team_1: str,
    team_2: str,
    label_1: str,
    label_2: str,
):
    fig, ax, pitch = create_vertical_pitch(half, v_size, h_size)  # noqa: F841
    team_1, team_2 = split_df(event_id, team_1, team_2)
    team_1_plot = create_scatter_plot_for_one_team(  # noqa: F841
        team_1, color_1, label_1, pitch, ax
    )
    team_2_plot = create_scatter_plot_for_one_team(  # noqa: F841
        team_2, color_2, label_2, pitch, ax
    )
    ax.legend()


def create_scatter_plot_with_goals_for_two_teams(
    event_id: str,
    half: bool,
    v_size: int,
    h_size: int,
    color_1: str,
    color_2: str,
    team_1: str,
    team_2: str,
    label_1: str,
    label_2: str,
):
    fig, ax, pitch = create_vertical_pitch(half, v_size, h_size)
    team_1, team_2 = split_df(event_id, team_1, team_2)
    team_1_g_df, team_1_ng_df = split_df_goals(team_1)
    team_2_g_df, team_2_ng_df = split_df_goals(team_2)
    team_1_plot_g = create_scatter_plot_for_one_team(  # noqa: F841
        team_1_g_df, color_1, label_1, pitch, ax, "football"
    )
    team_2_plot_g = create_scatter_plot_for_one_team(  # noqa: F841
        team_2_g_df, color_2, label_2, pitch, ax, "football"
    )
    team_1_plot_ng = create_scatter_plot_for_one_team(  # noqa: F841
        team_1_ng_df, color_1, label_1, pitch, ax, "s"
    )
    team_2_plot_ng = create_scatter_plot_for_one_team(  # noqa: F841
        team_2_ng_df, color_2, label_2, pitch, ax, "s"
    )  # noqa: F841

    ax.legend(labelspacing=2)


def create_scatter_plot_with_goals(
    event_id: str,
    half: bool,
    v_size: int,
    h_size: int,
    color_1: str,
    team_1: str,
    team_2: str,
    label_1: str,
):

    fig, ax, pitch = create_vertical_pitch(half, v_size, h_size)
    team_1, _ = split_df(event_id, team_1, team_2)
    team_1_g_df, team_1_ng_df = split_df_goals(team_1)
    team_1_plot_ng = create_scatter_plot_for_one_team(  # noqa: F841
        team_1_ng_df, color_1, label_1, pitch, ax, "s"
    )
    team_1_plot_g = create_scatter_plot_for_one_team(  # noqa: F841
        team_1_g_df, color_1, label_1, pitch, ax, "football"
    )  # noqa: F841

    ax.legend(labelspacing=2)
