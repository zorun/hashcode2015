import sys
from collections import defaultdict


class X(object):
    """Represents an unavailable slot"""
    def __str__(self):
        return 'X'


class Server(object):

    def __init__(self, size, cpu):
        self.size = size
        self.cpu = cpu
        self.pool = None
        self.row = None
        self.slot = None

    def output(self):
        if None in [self.pool, self.row, self.slot]:
            return 'x'
        else:
            return '{} {} {}'.format(self.row, self.slot, self.pool.id)

    def __str__(self):
        return 'Server({}, {}, {})'.format(self.size, self.cpu, self.pool.id)


class Row(object):

    def __init__(self, id, length):
        self.id = id
        self.length = length
        self.slots = [None] * length

    def add_unavailable(self, pos):
        self.slots[pos] = X()

    def add_server(self, serv, pos):
        #print("Add server to row {} at pos {}".format(self.id, pos))
        assert(pos >= 0)
        assert(pos + serv.size <= self.length)
        for i in range(pos, pos + serv.size):
            assert(self.slots[i] == None)
            self.slots[i] = serv
        serv.row = self.id
        serv.slot = pos
        if serv.pool != None:
            serv.pool.dirty = True

    def del_server(self, pos):
        serv = self.slots[pos]
        serv.row = None
        serv.slot = None
        for i in range(pos, pos + serv.size):
            self.slots[i] = None
        if serv.pool != None:
            serv.pool.dirty = True

    def allocate(self, size):
        """Yields positions at which a server of the given size can be placed"""
        for i in range(self.length):
            if self.slots[i:i+size] == [None]*size:
                yield i

    def display(self):
        for (i, x) in enumerate(self.slots):
            if x == None:
                print("[{}] ".format(i), end='')
            else:
                print("[{}] {} ".format(i, str(x)), end='')
        print()


class Pool(object):
    
    def __init__(self, id):
        self.id = id
        self.servers = set()
        self.cached_score = 0
        # For score caching
        self.dirty = False

    def add_server(self, serv):
        #print("Add server to pool {}".format(self.id))
        self.servers.add(serv)
        serv.pool = self
        self.dirty = True

    def del_server(self, serv):
        #print("Del server from pool {}".format(self.id))
        self.servers.remove(serv)
        serv.pool = None
        self.dirty = True

    @property
    def score(self):
        if self.dirty:
            self.cached_score = self.compute_score()
            self.dirty = False
        return self.cached_score

    def compute_score(self):
        if self.servers == set():
            return 0
        cpu = sum((s.cpu for s in self.servers))
        # CPU capacity per row
        cpu_row = defaultdict(int)
        for s in self.servers:
            cpu_row[s.row] += s.cpu
        #print(cpu_row)
        #print("Score for pool {} is {} with {} servers".format(self.id, cpu - max(cpu_row.values()), len(self.servers)))
        return cpu - max(cpu_row.values())


class DC(object):

    def __init__(self, input_file):
        with open(input_file) as f:
            self.nb_rows, self.nb_slots, self.nb_unavail, self.nb_pools, self.nb_servers = [int(x) for x in f.readline().split(' ')]
            self.rows = [Row(r, self.nb_slots) for r in range(self.nb_rows)]
            for i in range(self.nb_unavail):
                row, slot = [int(x) for x in f.readline().split(' ')]
                self.rows[row].add_unavailable(slot)
            self.servers = list()
            for i in range(self.nb_servers):
                size, cpu = [int(x) for x in f.readline().split(' ')]
                self.servers.append(Server(size, cpu))
        self.pools = [Pool(i) for i in range(self.nb_pools)]
                    

    def output(self, out=sys.stdout):
        for s in self.servers:
            print(s.output(), file=out)

    def score(self):
        return min((p.score for p in self.pools))

    def place_server(self, server, pool):
        """Place a server in a specific pool so that the score of this pool is
        maximised.  Test all possible rows.  Return None if not possible"""
        pool.add_server(server)
        max_score = 0
        optimal_place = (None, None)
        for r in self.rows:
            for pos in r.allocate(server.size):
                r.add_server(server, pos)
                if pool.score >= max_score:
                    optimal_place = (r, pos)
                    max_score = pool.score
                r.del_server(pos)
        if optimal_place == (None, None):
            pool.del_server(server)
            return None
        else:
            #print("Keeping optimal place {0[0].id}, {0[1]}".format(optimal_place))
            optimal_place[0].add_server(server, optimal_place[1])
            return optimal_place

    def solve(self):
        success = True
        while success:
            worst_pool = min(self.pools, key=lambda p: p.score)
            #print("Working on pool {}, score {}".format(worst_pool.id, worst_pool.score))
            available_servers = [s for s in self.servers if s.pool == None]
            if available_servers == []:
                return
            # Best server first
            for server in sorted(available_servers, key=lambda s: s.cpu / s.size, reverse=True):
                #print("Trying server {}".format(server))
                res = self.place_server(server, worst_pool)
                if res != None: # Success
                    success = True
                    #print("Success!")
                    break
            else:
                success = False
            #print(self.score(), [p.score for p in self.pools])

    def display(self):
        for (i, r) in enumerate(self.rows):
            print("Row {}".format(i))
            r.display()
                      


if __name__ == "__main__":
    d = DC(sys.argv[1])
    d.solve()
    #d.display()
    d.output()
    print(d.score(), file=sys.stderr)
