# scps_tree.py

from collections import defaultdict

class SCPSNode:
    def __init__(self, item_name, parent=None, is_tail=False):
        self.item = item_name
        self.count = 1
        self.parent = parent
        self.children = {}
        self.next = None  # link to same item
        self.is_tail = is_tail

        # Tail-node specific fields
        self.pre_count = 0
        self.cur_count = 0

    def increase_count(self, is_after_checkpoint):
        self.count += 1
        if self.is_tail:
            if is_after_checkpoint:
                self.cur_count += 1
            else:
                self.pre_count += 1

class SCPSTree:
    def __init__(self):
        self.root = SCPSNode("root")
        self.head_table = defaultdict(list)  # item -> list of nodes

    def insert_transaction(self, transaction, checkpoint_tid, current_tid):
        """
        Insert a transaction into the SCPS-tree, sorted by item frequency
        """
        sorted_items = self._sort_transaction(transaction)
        self._insert_path(sorted_items, checkpoint_tid, current_tid)

    def _insert_path(self, items, checkpoint_tid, current_tid):
        node = self.root
        for idx, item in enumerate(items):
            is_tail = idx == len(items) - 1
            if item in node.children:
                child = node.children[item]
                child.increase_count(current_tid > checkpoint_tid)
            else:
                child = SCPSNode(item_name=item, parent=node, is_tail=is_tail)
                if is_tail:
                    if current_tid > checkpoint_tid:
                        child.cur_count += 1
                    else:
                        child.pre_count += 1
                node.children[item] = child
                self.head_table[item].append(child)
            node = child

    def _sort_transaction(self, transaction):
        """
        Sort items by frequency in head_table (descending)
        Items not in head_table yet go to the end
        """
        freq_map = {item: sum(n.count for n in self.head_table[item]) for item in transaction if item in self.head_table}
        return sorted(transaction, key=lambda x: (-freq_map.get(x, 0), x))

    def print_tree(self, node=None, indent=0):
        if node is None:
            node = self.root
        for child in node.children.values():
            line = f"{'  ' * indent}- {child.item} [{child.count}]"
            if child.is_tail:
                line += f" (pre: {child.pre_count}, cur: {child.cur_count})"
            print(line)
            self.print_tree(child, indent + 1)



    def delete_expired_data(self):
        print("🧹 Deleting expired data (before checkpoint)...")

        # Sort items by total support ascending (least supported first)
        sorted_items = sorted(self.head_table.keys(), key=lambda x: sum(n.count for n in self.head_table[x]))

        for item in sorted_items:
            for node in list(self.head_table[item]):  # use a copy of the list
                if not node.is_tail:
                    continue

                current = node
                path = []
                while current and current.parent:
                    path.append(current)
                    current = current.parent

                for n in path:
                    n.count -= node.pre_count
                    if n.count <= 0:
                        if n.parent:
                            del n.parent.children[n.item]
                        self.head_table[n.item].remove(n)

                # Update tail counts
                node.pre_count = node.cur_count
                node.cur_count = 0

        # You can optionally re-balance with BSM here (if you implement it)


