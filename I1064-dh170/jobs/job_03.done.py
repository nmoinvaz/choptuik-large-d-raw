rec = ls.run(ctx, dict(axes="1", emin="-30", emax="-26", estep="2"))
print("points:", [(p["ax"], p["e"], p["ok"], p["why"]) for p in rec["points"]])
