import sys
from collections import deque

def solve(edges: list[tuple[str, str]]) -> list[str]:
	adj: dict[str, set[str]] = {}

	for a, b in edges:
		adj.setdefault(a, set()).add(b)
		adj.setdefault(b, set()).add(a)

	if "a" not in adj:
		print("Ошибка ввода: отсутствует стартовый узел 'a'")
		sys.exit(1)

	virus = "a"
	result: list[str] = []

	def bfs(start: str):
		dist = {start: 0}
		q = deque([start])
		while q:
			cur = q.popleft()
			for nxt in sorted(adj.get(cur, [])):
				if nxt not in dist:
					dist[nxt] = dist[cur] + 1
					q.append(nxt)
		return dist

	def all_gateways():
		return sorted([x for x in adj if x.isupper()])

	def find_path(start: str, target: str):
		q = deque([start])
		prev = {start: None}
		while q:
			cur = q.popleft()
			if cur == target:
				break
			for nxt in sorted(adj[cur]):
				if nxt not in prev:
					prev[nxt] = cur
					q.append(nxt)
		if target not in prev:
			return []
		path = []
		cur = target
		while cur is not None:
			path.append(cur)
			cur = prev[cur]
		return path[::-1]

	while True:
		dist = bfs(virus)

		reachable = [(g, dist[g]) for g in all_gateways() if g in dist]
		if not reachable:
			break

		min_d = min(d for _, d in reachable)
		target_gate = sorted([g for g, d in reachable if d == min_d])[0]
		path = find_path(virus, target_gate)
		if len(path) < 2:
			break 
		candidates = []
		for g in all_gateways():
			for n in sorted(adj[g]):
				if n.islower():
					candidates.append(f"{g}-{n}")
		if not candidates:
			break

		to_block = min(candidates)
		g, n = to_block.split("-")
		if g in adj and n in adj[g]:
			adj[g].remove(n)
		if n in adj and g in adj[n]:
			adj[n].remove(g)
		result.append(to_block)

		new_dist = bfs(virus)
		if target_gate not in new_dist:
			continue

		path = find_path(virus, target_gate)
		if len(path) >= 2:
			virus = path[1]
		else:
			break

	return result


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
