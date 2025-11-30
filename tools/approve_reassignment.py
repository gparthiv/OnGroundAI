from google.adk.tools.tool_context import ToolContext

def approve_reassignment(
    worker_id: str, 
    old_task: str, 
    new_task: str, 
    tool_context: ToolContext
) -> dict:
    """
    Requests supervisor approval before reassigning a worker to a new task.
    
    Args:
        worker_id: ID of the worker to reassign
        old_task: Current task ID
        new_task: New task ID
        tool_context: ADK tool context for pause/resume
    
    Returns:
        Dictionary with status and message
    """
    
    # Scenario 1: First call - Request approval (PAUSE)
    if not tool_context.tool_confirmation:
        tool_context.request_confirmation(
            hint=f"Reassign Worker {worker_id}?\nFrom: {old_task}\nTo: {new_task}",
            payload={"worker_id": worker_id, "new_task": new_task}
        )
        return {
            "status": "pending_approval",
            "message": f"Awaiting supervisor approval for {worker_id} reassignment"
        }
    
    # Scenario 2: Second call - Approval received (RESUME)
    if tool_context.tool_confirmation.confirmed:
        return {
            "status": "approved",
            "message": f"Worker {worker_id} reassigned to {new_task}",
            "action": "reassignment_completed"
        }
    else:
        return {
            "status": "rejected",
            "message": f"Reassignment cancelled by supervisor",
            "action": "reassignment_cancelled"
        }