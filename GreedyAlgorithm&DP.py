import bisect

class Job:
    def __init__(self, job_id, start, finish, weight):
        self.job_id = job_id
        self.start  = start
        self.finish = finish
        self.weight = weight

    def __repr__(self):
        return f"Job(id={self.job_id}, start={self.start}, finish={self.finish}, weight={self.weight})"

class GreedyScheduler:
    def __init__(self, jobs):
        self.jobs = jobs

    def schedule(self):
        
        sorted_jobs = sorted(self.jobs, key=lambda j: j.finish)

        selected = []
        last_finish = 0

        for job in sorted_jobs:
            if job.start >= last_finish:
                selected.append(job)
                last_finish = job.finish

        total_weight = sum(j.weight for j in selected)
        return selected, total_weight

    def print_time_complexity(self):
        print("Greedy Time Complexity:")
        print("  Sort by finish time : O(n log n)")
        print("  Linear scan         : O(n)")
        print("  Overall             : O(n log n)")


class DPScheduler:
    def __init__(self, jobs):
        self.jobs = jobs

    def find_p(self, sorted_jobs):
    
        finish_times = [j.finish for j in sorted_jobs]
        n = len(sorted_jobs)
        p = [0] * (n + 1)
        for i in range(1, n + 1):
            idx = bisect.bisect_right(finish_times, sorted_jobs[i-1].start, 0, i-1)
            p[i] = idx
        return p

    def schedule(self):
        
        sorted_jobs = sorted(self.jobs, key=lambda j: j.finish)
        n = len(sorted_jobs)

        p = self.find_p(sorted_jobs)

        opt = [0.0] * (n + 1)
        for i in range(1, n + 1):
            include = sorted_jobs[i-1].weight + opt[p[i]]
            exclude = opt[i-1]
            opt[i] = max(include, exclude)

        selected = []
        i = n
        while i >= 1:
            if sorted_jobs[i-1].weight + opt[p[i]] >= opt[i-1]:
                selected.append(sorted_jobs[i-1])
                i = p[i]
            else:
                i -= 1
        selected.reverse()

        return selected, opt[n]

    def print_time_complexity(self):
        print("DP Time Complexity:")
        print("  Sort by finish time          : O(n log n)")
        print("  Compute p(i) (binary search) : O(n log n)")
        print("  Fill DP table                : O(n)")
        print("  Traceback                    : O(n)")
        print("  Overall                      : O(n log n)")


if __name__ == "__main__":
    jobs = [
        Job(1, 1,  4,  3),
        Job(2, 3,  5,  4),
        Job(3, 0,  6,  8),
        Job(4, 4,  7,  2),
        Job(5, 3,  8,  1),
        Job(6, 5,  9,  6),
        Job(7, 6, 10,  5),
        Job(8, 8, 11,  4),
    ]

    print("Input Jobs:")
    for j in jobs:
        print(" ", j)

    print()

    print("=== Greedy (Activity Selection) ===")
    greedy = GreedyScheduler(jobs)
    g_selected, g_weight = greedy.schedule()
    print("Selected:", [j.job_id for j in g_selected])
    print("Total Weight:", g_weight)
    greedy.print_time_complexity()

    print()

    print("=== DP (Weighted Interval Scheduling) ===")
    dp = DPScheduler(jobs)
    d_selected, d_weight = dp.schedule()
    print("Selected:", [j.job_id for j in d_selected])
    print("Total Weight:", d_weight)
    dp.print_time_complexity()
