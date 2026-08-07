import os
import pytest
from harness.continual_memory import ContinualMemoryManager, TrajectoryTelemetry
from harness.rlm_orchestrator import RLMContextPartitioning
from harness.autonomous_loop import AutonomousHarnessController

def test_continual_memory_manager(tmp_path):
    mem_file = str(tmp_path / "test_memory.json")
    manager = ContinualMemoryManager(memory_file_path=mem_file)
    assert manager.state["version"] == "1.0.0"
    
    telemetry = TrajectoryTelemetry(
        project_id="test_proj_001",
        topic="Test Harness Topic",
        fact_check_score=100.0,
        verified_citations=10,
        broken_citations=0,
        grounded_metrics=5,
        unverified_metrics=0,
        duration_seconds=12.5,
        timestamp=1000.0
    )
    result = manager.record_telemetry(telemetry)
    assert result["success"] is True
    assert manager.state["total_runs"] == 1
    assert os.path.exists(mem_file)

def test_rlm_context_partitioning():
    rlm = RLMContextPartitioning(max_batch_size=5)
    papers = [{"title": f"Paper {i}"} for i in range(12)]
    batches = rlm.partition_corpus(papers)
    assert len(batches) == 3
    assert len(batches[0]) == 5
    assert len(batches[2]) == 2
    
    summary = rlm.summarize_sub_agent_batch(0, batches[0])
    assert summary["paper_count"] == 5
    assert summary["batch_index"] == 0

def test_autonomous_harness_controller():
    controller = AutonomousHarnessController()
    controller.register_task("proj_123", "AI Enterprise")
    status = controller.get_task_status("proj_123")
    assert status["status"] == "started"
    
    controller.update_heartbeat("proj_123", "Analyst PDF Extraction", 40.0)
    status = controller.get_task_status("proj_123")
    assert status["progress_percent"] == 40.0
    
    controller.complete_task("proj_123")
    status = controller.get_task_status("proj_123")
    assert status["status"] == "completed"
