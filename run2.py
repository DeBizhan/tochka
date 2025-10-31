import sys
from collections import deque
from functools import lru_cache

def normalize_edges(edges):
	s = set()
	for a, b in edges:
		s.add((a, b) if a <= b else (b, a))
	return frozenset(s)

def build_adj(edges_frozen):
	adj = {}
	for a, b in edges_frozen:
		adj.setdefault(a, set()).add(b)
		adj.setdefault(b, set()).add(a)
	return adj

def bfs_with_prev(start, adj):
	dist = {start: 0}
	prev = {start: None}
	q = deque([start])
	while q:
		cur = q.popleft()
		for nxt in sorted(adj.get(cur, [])):
			if nxt not in dist:
				dist[nxt] = dist[cur] + 1
				prev[nxt] = cur
				q.append(nxt)
	return dist, prev

def next_step_on_shortest(virus, target, adj):
	dist, prev = bfs_with_prev(virus, adj)
	if target not in prev:
		return None
	path = []
	cur = target
	while cur is not None:
		path.append(cur)
		cur = prev[cur]
	path.reverse()
	return path[1] if len(path) >= 2 else None

def gateways_in_adj(adj):
	return sorted([n for n in adj.keys() if n.isupper()])

@lru_cache(maxsize=None)
def solve_state(edges_tuple, virus):
	edges_frozen = frozenset(edges_tuple)
	adj = build_adj(edges_frozen)
	dist, _ = bfs_with_prev(virus, adj)
	reachable_gates = [g for g in gateways_in_adj(adj) if g in dist]
	if not reachable_gates:
		return ()
	min_d = min(dist[g] for g in reachable_gates)
	target_candidates = sorted([g for g in reachable_gates if dist[g] == min_d])
	target_gate = target_candidates[0]
	candidates = []
	for g in gateways_in_adj(adj):
		for n in sorted(adj.get(g, [])):
			if n.islower():
				candidates.append(f"{g}-{n}")
	if not candidates:
		return None
	for cand in sorted(candidates):
		g, n = cand.split("-")
		key = (g, n) if g <= n else (n, g)
		if key not in edges_frozen:
			continue
		new_edges = set(edges_frozen)
		new_edges.remove(key)
		new_edges_t = tuple(sorted(new_edges))
		new_adj = build_adj(frozenset(new_edges_t))
		dist_after, _ = bfs_with_prev(virus, new_adj)
		reachable_after = [gg for gg in gateways_in_adj(new_adj) if gg in dist_after]
		if not reachable_after:
			return (cand,)
		min_d_a = min(dist_after[gg] for gg in reachable_after)
		tgt_candidates_a = sorted([gg for gg in reachable_after if dist_after[gg] == min_d_a])
		tgt_a = tgt_candidates_a[0]
		nxt = next_step_on_shortest(virus, tgt_a, new_adj)
		if nxt is None:
			return (cand,)
		if nxt.isupper():
			continue
		sub = solve_state(tuple(sorted(new_edges_t)), nxt)
		if sub is None:
			continue
		return (cand,) + sub
	return None

def solve(edges):
	if "a" not in {x for e in edges for x in e}:
		print("Ошибка ввода: отсутствует стартовый узел 'a'")
		sys.exit(1)
	norm = normalize_edges(edges)
	res = solve_state(tuple(sorted(norm)), "a")
	return list(res) if res else []

def main():
	edges = []
	for line in sys.stdin:
		line = line.strip()
		if not line:
			continue
		if '-' not in line:
			print("Ошибка ввода: строка без разделителя '-'")
			return
		a, b = line.split('-', 1)
		a, b = a.strip(), b.strip()
		if not a or not b:
			print("Ошибка ввода: некорректная пара узлов")
			return
		edges.append((a, b))
	if not edges:
		print("Ошибка ввода: пустые данные")
		return
	result = solve(edges)
	for r in result:
		print(r)

if __name__ == "__main__":
	main()
