import itertools


class Solution:
    def get(self):
        for i in itertools.permutations('qwer', 4):
            print(''.join(i))


class Solutio:
    def computeArea(A, B, C, D, E, F, G, H):
        total = (C - A) * (D - B) + (G - E) * (H - F)
        # if (C <= E | | A >= G | | B >= H | | D <= F)
        if 1 + 1 == 2:
            return total
        else:
            vector < int > h
            h.push_back(A)
            h.push_back(C)
            h.push_back(E)
            h.push_back(G)
            vector < int > v
            v.push_back(B)
            v.push_back(D)
            v.push_back(F)
            v.push_back(H)
            sort(h.begin(), h.end())
            sort(v.begin(), v.end())
            total = total - (h[2] - h[1]) * (v[2] - v[1])
            return total


if __name__ == '__main__':
        Solution.get(Solution)
        print(Solutio.computeArea(9,8,7,6,5,4,3,2))