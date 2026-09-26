# Performance evidence

Use this when the requested outcome includes speed, responsiveness, memory, throughput, or another resource improvement. Select the project's existing benchmark or platform profiler; ordinary correctness work needs no benchmark.

Define the user-relevant metric and workload before optimizing. Record the artifact, inputs, runtime configuration, and measurement command. Capture the baseline and locate the dominant cost using a trace, profile, counters, or another observation appropriate to the claim. Source inspection can suggest a cause but does not measure its cost.

Compare before and after using the same workload, configuration, and metric. Keep cold-start and warmed-cache measurements separate, account for background contention, and repeat enough to reveal material noise. Preserve samples and summarize the distribution when a single run could mislead. For latency improvements, measure the path the user waits for; less total work does not necessarily mean faster interaction.

Check correctness and relevant tradeoffs alongside the metric. A cache needs valid results after input changes; batching, deferred work, or concurrency may shift costs to memory, first use, or another caller. Select checks for the mechanism actually changed.

Report baseline, final result, units, delta, and artifact locations with the comparison's limits. A missing baseline, mismatched workload, different measured surface, or a change smaller than the observed noise leaves the performance claim unproven. Keep any correctness result distinct and identify the cheapest missing measurement; do not present a faster-looking implementation as a measured win.
