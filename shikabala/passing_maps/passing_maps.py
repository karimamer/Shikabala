from typing import Tuple
import statsbomb as sb
import pandas as pd

from mplsoccer import VerticalPitch


def get_event(event_id: str) -> object:
    events = sb.Events(event_id=event_id)
    return events


def get_df_for_event(event_id: str, event_type: str) -> pd.DataFrame:
    events = get_event(event_id)
    df = events.get_dataframe(event_type=event_type)
    return df


def split_df(
    event_id: str, team_1: str, team_2: str, event_type: str
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    df = get_df_for_event(event_id, event_type)
    team_1_df = df[df["team"] == team_1].copy()
    team_2_df = df[df["team"] == team_2].copy()
    return team_1_df, team_2_df


def create_vertical_pitch(v_size: int, h_size: int):
    pitch = VerticalPitch(half=False)
    fig, ax = pitch.draw(figsize=(v_size, h_size))
    return fig, ax, pitch


def create_scatter_plot_event(
    event_id: str, v_size: int, h_size: int, color: str
):
    df = get_df_for_event(event_id, "shot")
    fig, ax, pitch = create_vertical_pitch(v_size, h_size)
    sc = pitch.scatter(  # noqa: F841
        df["start_location_x"],
        df["start_location_y"],
        s=df["statsbomb_xg"] * 500 + 100,
        cmap=color,
        c=df["statsbomb_xg"],
        ax=ax,
    )
    return sc
