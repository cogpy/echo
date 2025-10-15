"""
Garden of Memory - Memory Synchronization Protocol
Coordinates memory access across multiple framework membranes
"""

import threading
from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass
from datetime import datetime
import json

from hypergraph import HypergraphMemory, IdentityFragment, RefinementTuple, IdentityAspect, RefinementType


@dataclass
class MemoryTransaction:
    """Represents a memory operation transaction"""
    transaction_id: str
    framework: str
    operation: str  # "add_fragment", "add_tuple", "retrieve", "update"
    timestamp: str
    data: Dict[str, Any]
    status: str  # "pending", "completed", "failed"


class MemorySyncProtocol:
    """
    Thread-safe memory synchronization protocol for multi-framework access
    Implements ACID-like properties for hypergraph operations
    """
    
    def __init__(self, memory: HypergraphMemory, log_file: str = "./data/memory_sync.log"):
        self.memory = memory
        self.log_file = log_file
        self.lock = threading.RLock()  # Reentrant lock for nested operations
        self.transactions: List[MemoryTransaction] = []
        self.subscribers: Dict[str, List[Callable]] = {}  # event -> callbacks
        
    def add_fragment_sync(self,
                          framework: str,
                          aspect: IdentityAspect,
                          content: str,
                          confidence: float,
                          keywords: List[str] = None,
                          metadata: Dict[str, Any] = None) -> Optional[str]:
        """
        Thread-safe fragment addition with transaction logging
        """
        with self.lock:
            try:
                # Create transaction
                import uuid
                transaction_id = str(uuid.uuid4())
                transaction = MemoryTransaction(
                    transaction_id=transaction_id,
                    framework=framework,
                    operation="add_fragment",
                    timestamp=datetime.now().isoformat(),
                    data={
                        "aspect": aspect.value,
                        "content": content,
                        "confidence": confidence,
                        "keywords": keywords,
                        "metadata": metadata
                    },
                    status="pending"
                )
                self.transactions.append(transaction)
                
                # Execute operation
                fragment_id = self.memory.add_fragment(
                    framework=framework,
                    aspect=aspect,
                    content=content,
                    confidence=confidence,
                    keywords=keywords,
                    metadata=metadata
                )
                
                # Update transaction status
                transaction.status = "completed"
                transaction.data["fragment_id"] = fragment_id
                
                # Log transaction
                self._log_transaction(transaction)
                
                # Notify subscribers
                self._notify("fragment_added", {
                    "fragment_id": fragment_id,
                    "framework": framework,
                    "aspect": aspect.value
                })
                
                return fragment_id
                
            except Exception as e:
                transaction.status = "failed"
                transaction.data["error"] = str(e)
                self._log_transaction(transaction)
                return None
    
    def add_refinement_tuple_sync(self,
                                   parent_id: Optional[str],
                                   child_id: str,
                                   refinement_type: RefinementType,
                                   confidence_gain: float,
                                   metadata: Dict[str, Any] = None) -> Optional[str]:
        """
        Thread-safe refinement tuple addition
        """
        with self.lock:
            try:
                import uuid
                transaction_id = str(uuid.uuid4())
                transaction = MemoryTransaction(
                    transaction_id=transaction_id,
                    framework="sync_protocol",
                    operation="add_tuple",
                    timestamp=datetime.now().isoformat(),
                    data={
                        "parent_id": parent_id,
                        "child_id": child_id,
                        "refinement_type": refinement_type.value,
                        "confidence_gain": confidence_gain
                    },
                    status="pending"
                )
                self.transactions.append(transaction)
                
                tuple_id = self.memory.add_refinement_tuple(
                    parent_id=parent_id,
                    child_id=child_id,
                    refinement_type=refinement_type,
                    confidence_gain=confidence_gain,
                    metadata=metadata
                )
                
                transaction.status = "completed"
                transaction.data["tuple_id"] = tuple_id
                self._log_transaction(transaction)
                
                self._notify("tuple_added", {
                    "tuple_id": tuple_id,
                    "parent_id": parent_id,
                    "child_id": child_id
                })
                
                return tuple_id
                
            except Exception as e:
                transaction.status = "failed"
                transaction.data["error"] = str(e)
                self._log_transaction(transaction)
                return None
    
    def retrieve_sync(self,
                      query: str,
                      aspect: Optional[IdentityAspect] = None,
                      framework: Optional[str] = None,
                      top_k: int = 5) -> List[IdentityFragment]:
        """
        Thread-safe retrieval with read lock
        """
        with self.lock:
            return self.memory.retrieve_similar(
                query=query,
                aspect=aspect,
                framework=framework,
                top_k=top_k
            )
    
    def batch_add_fragments(self,
                            fragments: List[Dict[str, Any]]) -> List[str]:
        """
        Batch addition of fragments (atomic operation)
        """
        with self.lock:
            fragment_ids = []
            for frag_data in fragments:
                fid = self.add_fragment_sync(
                    framework=frag_data["framework"],
                    aspect=IdentityAspect(frag_data["aspect"]),
                    content=frag_data["content"],
                    confidence=frag_data["confidence"],
                    keywords=frag_data.get("keywords"),
                    metadata=frag_data.get("metadata")
                )
                if fid:
                    fragment_ids.append(fid)
            return fragment_ids
    
    def subscribe(self, event_type: str, callback: Callable):
        """
        Subscribe to memory events
        
        Args:
            event_type: "fragment_added", "tuple_added", "memory_saved"
            callback: Function to call when event occurs
        """
        if event_type not in self.subscribers:
            self.subscribers[event_type] = []
        self.subscribers[event_type].append(callback)
    
    def _notify(self, event_type: str, data: Dict[str, Any]):
        """Notify all subscribers of an event"""
        if event_type in self.subscribers:
            for callback in self.subscribers[event_type]:
                try:
                    callback(data)
                except Exception as e:
                    print(f"Error in subscriber callback: {e}")
    
    def _log_transaction(self, transaction: MemoryTransaction):
        """Log transaction to file"""
        try:
            with open(self.log_file, 'a') as f:
                log_entry = {
                    "transaction_id": transaction.transaction_id,
                    "framework": transaction.framework,
                    "operation": transaction.operation,
                    "timestamp": transaction.timestamp,
                    "status": transaction.status,
                    "data": transaction.data
                }
                f.write(json.dumps(log_entry) + "\n")
        except Exception as e:
            print(f"Error logging transaction: {e}")
    
    def save_checkpoint(self, filepath: str):
        """
        Save memory checkpoint with transaction log
        """
        with self.lock:
            self.memory.save(filepath)
            self._notify("memory_saved", {"filepath": filepath})
    
    def load_checkpoint(self, filepath: str):
        """
        Load memory checkpoint
        """
        with self.lock:
            self.memory.load(filepath)
            self._notify("memory_loaded", {"filepath": filepath})
    
    def get_transaction_history(self, 
                                 framework: Optional[str] = None,
                                 limit: int = 100) -> List[MemoryTransaction]:
        """Get transaction history, optionally filtered by framework"""
        with self.lock:
            transactions = self.transactions
            if framework:
                transactions = [t for t in transactions if t.framework == framework]
            return transactions[-limit:]
    
    def get_sync_statistics(self) -> Dict[str, Any]:
        """Get synchronization statistics"""
        with self.lock:
            total_transactions = len(self.transactions)
            completed = sum(1 for t in self.transactions if t.status == "completed")
            failed = sum(1 for t in self.transactions if t.status == "failed")
            
            framework_stats = {}
            for transaction in self.transactions:
                fw = transaction.framework
                if fw not in framework_stats:
                    framework_stats[fw] = {"total": 0, "completed": 0, "failed": 0}
                framework_stats[fw]["total"] += 1
                if transaction.status == "completed":
                    framework_stats[fw]["completed"] += 1
                elif transaction.status == "failed":
                    framework_stats[fw]["failed"] += 1
            
            return {
                "total_transactions": total_transactions,
                "completed_transactions": completed,
                "failed_transactions": failed,
                "success_rate": completed / total_transactions if total_transactions > 0 else 0.0,
                "framework_statistics": framework_stats,
                "memory_statistics": self.memory.get_statistics()
            }


class FrameworkMemoryInterface:
    """
    Simplified interface for frameworks to interact with Garden of Memory
    Abstracts away synchronization complexity
    """
    
    def __init__(self, framework_name: str, sync_protocol: MemorySyncProtocol):
        self.framework_name = framework_name
        self.sync = sync_protocol
    
    def remember(self,
                 aspect: IdentityAspect,
                 content: str,
                 confidence: float,
                 keywords: List[str] = None) -> Optional[str]:
        """
        Store a memory fragment
        """
        return self.sync.add_fragment_sync(
            framework=self.framework_name,
            aspect=aspect,
            content=content,
            confidence=confidence,
            keywords=keywords
        )
    
    def recall(self,
               query: str,
               aspect: Optional[IdentityAspect] = None,
               top_k: int = 5) -> List[IdentityFragment]:
        """
        Retrieve relevant memories
        """
        return self.sync.retrieve_sync(
            query=query,
            aspect=aspect,
            framework=self.framework_name,
            top_k=top_k
        )
    
    def refine(self,
               parent_id: str,
               child_id: str,
               refinement_type: RefinementType,
               confidence_gain: float) -> Optional[str]:
        """
        Create a refinement tuple
        """
        return self.sync.add_refinement_tuple_sync(
            parent_id=parent_id,
            child_id=child_id,
            refinement_type=refinement_type,
            confidence_gain=confidence_gain
        )
    
    def get_my_memories(self, top_k: int = 10) -> List[IdentityFragment]:
        """
        Get this framework's memories
        """
        return self.sync.memory.retrieve_by_framework(
            framework=self.framework_name,
            top_k=top_k
        )


if __name__ == "__main__":
    # Example usage
    from hypergraph import HypergraphMemory
    
    # Initialize
    memory = HypergraphMemory()
    sync = MemorySyncProtocol(memory)
    
    # Create framework interfaces
    openhands = FrameworkMemoryInterface("OpenHands", sync)
    ii_researcher = FrameworkMemoryInterface("ii-researcher", sync)
    
    # Subscribe to events
    def on_fragment_added(data):
        print(f"New fragment added: {data['fragment_id']} from {data['framework']}")
    
    sync.subscribe("fragment_added", on_fragment_added)
    
    # Frameworks store memories
    print("=== Storing Memories ===\n")
    
    fid1 = openhands.remember(
        aspect=IdentityAspect.TECHNICAL_CAPABILITY,
        content="Generated Python code for data processing",
        confidence=0.85
    )
    
    fid2 = ii_researcher.remember(
        aspect=IdentityAspect.KNOWLEDGE_DOMAIN,
        content="Research on transformer architectures",
        confidence=0.78
    )
    
    # Retrieve memories
    print("\n=== Recalling Memories ===\n")
    
    results = openhands.recall("python code", top_k=3)
    for frag in results:
        print(f"  - {frag.content} (confidence: {frag.confidence})")
    
    # Print statistics
    print("\n=== Sync Statistics ===")
    print(json.dumps(sync.get_sync_statistics(), indent=2))

