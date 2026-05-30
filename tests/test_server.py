from forecast_mcp.server import backtest
import pytest

def test_backtest_baseline():
    # Provide enough points for a 6-point holdout + 3 points
    series = [10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30, 32]
    res = backtest(series, holdout=4)
    
    assert res["holdout"] == 4
    assert "baseline" in res["results"]
    assert "mae" in res["results"]["baseline"]
    assert "mae" in res["results"]["baseline"]
    assert "smape" in res["results"]["baseline"]
    
def test_backtest_too_few_points():
    with pytest.raises(ValueError, match="Need at least 6 observations"):
        backtest([1, 2, 3, 4, 5], holdout=3)

def test_backtest_small_values():
    # Provide enough points of near-zero values to ensure sMAPE doesn't crash
    series = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.001]
    res = backtest(series, holdout=4)
    
    assert "error" not in res["results"]["baseline"]
    assert res["results"]["baseline"]["smape"] >= 0
