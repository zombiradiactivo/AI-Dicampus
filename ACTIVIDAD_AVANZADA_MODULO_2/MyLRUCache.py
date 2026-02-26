from __future__ import annotations
from typing import Dict, Optional

class Node:
    def __init__(self, key: int, value: int):
        self.key: int = key
        self.value: int = value
        # Inicializamos con tipo Node | None
        self.prev: Node | None = None
        self.next: Node | None = None

class LRUCache:
    def __init__(self, capacity: int):
        self.cap: int = capacity
        self.cache: Dict[int, Node] = {}

        # Nodos centinela: head y tail siempre existen
        self.head: Node = Node(0, 0)
        self.tail: Node = Node(0, 0)
        
        # Conexión inicial: head <-> tail
        self.head.next = self.tail
        self.tail.prev = self.head

    def _remove(self, node: Node) -> None:
        """Elimina un nodo. El linter requiere 'assert' o chequeo para asegurar que no son None."""
        prev_node = node.prev
        next_node = node.next
        
        if prev_node and next_node:
            prev_node.next = next_node
            next_node.prev = prev_node

    def _add(self, node: Node) -> None:
        """Añade el nodo justo después de la cabeza."""
        # head.next siempre existe (mínimo es tail)
        first_node = self.head.next
        if first_node:
            node.next = first_node
            node.prev = self.head
            self.head.next = node
            first_node.prev = node

    def get(self, key: int) -> int:
        if key in self.cache:
            node = self.cache[key]
            self._remove(node)
            self._add(node)
            return node.value
        return -1

    def put(self, key: int, value: int) -> None:
        if key in self.cache:
            self._remove(self.cache[key])
        
        new_node = Node(key, value)
        self.cache[key] = new_node
        self._add(new_node)
        
        if len(self.cache) > self.cap:
            # El LRU es el nodo justo antes de tail
            lru_node = self.tail.prev
            if lru_node and lru_node != self.head:
                self._remove(lru_node)
                del self.cache[lru_node.key]