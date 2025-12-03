// API Configuration
const API_BASE_URL = 'https://ongroundai-backend.onrender.com';

// Global State
let currentSessionId = 'workflow-session';
let workflowStartTime = null;
let agentsCompleted = 0;
let executionLog = [];

// Initialize Dashboard
document.addEventListener('DOMContentLoaded', async () => {
    console.log('Dashboard initializing...');
    await initializeDashboard();
    setupEventListeners();
});

// Initialize Dashboard - Load Data
async function initializeDashboard() {
    try {
        console.log('Fetching data from backend...');
        // Load worker data
        const dataResponse = await fetch(`${API_BASE_URL}/api/data`);
        const data = await dataResponse.json();
        console.log('Data received:', data);
        if (data.success) {
            // Pass arrays (workers, tasks, messages)
            displayWorkerCards(data.workers || [], data.tasks || [], data.messages || []);
            // Save the data lengths for DataIngestAgent simulation
            window.__initial_data_counts = {
                workers: (data.workers || []).length,
                tasks: (data.tasks || []).length,
                messages: (data.messages || []).length,
                calendar: (data.calendar || []).length
            };
            console.log('Worker cards displayed');
        } else {
            console.error(' Data fetch failed:', data.error);
        }

        // Load tools registry
        const toolsResponse = await fetch(`${API_BASE_URL}/api/tools`);
        const tools = await toolsResponse.json();
        console.log('Tools received:', tools);
        if (tools.success) {
            displayToolRegistry(tools.tools || []);
            console.log('Tool registry displayed');
        } else {
            console.error(' Tools fetch failed:', tools.error);
        }

        // Update session info
        updateSessionInfo(currentSessionId);

        // Add initial log entry
        addExecutionLog('Dashboard loaded successfully', new Date());

    } catch (error) {
        console.error(' Error initializing dashboard:', error);
        addExecutionLog(' Error loading dashboard: ' + (error.message || error), new Date());
    }
}


// Setup Event Listeners
function setupEventListeners() {
    const chatInput = document.getElementById('chat-input');
    const chatSendBtn = document.getElementById('chat-send');

    // Send button click
    chatSendBtn.addEventListener('click', handleChatSend);

    // Enter key in chat input
    chatInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            handleChatSend();
        }
    });

    console.log('Event listeners setup complete');
}

// Handle Chat Send
async function handleChatSend() {
    const chatInput = document.getElementById('chat-input');
    const message = chatInput.value.trim();

    if (!message) return;

    console.log('Sending message:', message);

    // Add user message to chat
    addChatMessage(message, 'user');
    chatInput.value = '';

    // Add loading indicator
    const loadingBubble = addChatMessage('Thinking...', 'agent', true);

    try {
        console.log('Posting to /run_agent...');

        const response = await fetch(`${API_BASE_URL}/run_agent`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ message: message }),
        });

        const data = await response.json();
        console.log('Response received:', data);

        // Remove loading indicator
        if (loadingBubble && loadingBubble.parentNode) {
            loadingBubble.parentNode.removeChild(loadingBubble);
        }

        if (data.success) {
            // Check if workflow was triggered
            if (data.workflow_triggered) {
                console.log('Workflow triggered!');

                // Update session ID
                if (data.session_id) {
                    currentSessionId = data.session_id;
                    updateSessionInfo(currentSessionId);
                }

                // Add workflow started message
                addChatMessage('Starting workflow analysis...', 'agent');

                // Start workflow execution simulation
                await executeWorkflow(data);
            } else {
                console.log('Regular chat response');
                // Regular chat response
                addChatMessage(data.response || 'No response', 'agent');
            }
        } else {
            console.error(' API Error:', data.error);
            addChatMessage('Error: ' + (data.error || 'Unknown error'), 'agent');
        }
    } catch (error) {
        console.error(' Error sending message:', error);

        // Remove loading indicator
        if (loadingBubble && loadingBubble.parentNode) {
            loadingBubble.parentNode.removeChild(loadingBubble);
        }

        addChatMessage('Error connecting to backend. Please check if the server is running on port 8000.', 'agent');
    }
}

// Execute Workflow
async function executeWorkflow(workflowData) {
    console.log('Starting workflow execution...');

    workflowStartTime = Date.now();
    agentsCompleted = 0;
    executionLog = [];

    // Clear previous execution log
    document.getElementById('execution-log').innerHTML = '';

    // Add workflow started log
    addExecutionLog('WORKFLOW STARTED', new Date());

    // Simulate DataIngestAgent
    console.log('▶️ DataIngestAgent starting...');
    await simulateAgentExecution('DataIngestAgent', async () => {
        updateAgentStatus('dataingest', 'running');
        addExecutionLog('DataIngestAgent → Started', new Date());

        const counts = window.__initial_data_counts || { messages: 3, calendar: 2, tasks: 2 };

        await delay(400);
        addExecutionLog(`load_messages() → Success (${counts.messages} items)`, new Date());

        await delay(400);
        addExecutionLog(`load_calendar() → Success (${counts.calendar} items)`, new Date());

        await delay(400);
        addExecutionLog(`load_tasks() → Success (${counts.tasks} items)`, new Date());

        // Update UI - report times roughly (you can compute exact if desired)
        document.getElementById('dataingest-status').textContent = '✓ Complete (1.2s)';
        document.getElementById('dataingest-status').classList.add('complete');
        document.getElementById('dataingest-tools').textContent = '3';

        const dataHtml = `
            <div class="agent-data-item">• load_messages → ${counts.messages} items</div>
            <div class="agent-data-item">• load_calendar → ${counts.calendar} items</div>
            <div class="agent-data-item">• load_tasks → ${counts.tasks} items</div>
        `;
        document.getElementById('dataingest-data').innerHTML = dataHtml;

        agentsCompleted++;
        // If backend returned agents_completed, sync it
        if (window.__backend_agents_completed) {
            agentsCompleted = Math.max(agentsCompleted, window.__backend_agents_completed);
        }
        updateHeaderStats();
    }, 1200);


    console.log('▶️ Starting parallel execution...');
    addExecutionLog('🔀 Starting DelayAgent & SafetyAgent in parallel...', new Date());

    // Simulate Parallel Execution (DelayAgent and SafetyAgent)
    const parallelPromises = [];

    // DelayAgent
    parallelPromises.push(
        simulateAgentExecution('DelayAgent', async () => {
            updateAgentStatus('delay', 'running');
            addExecutionLog('⏰ DelayAgent → Analyzing delays...', new Date());

            // Parse delay findings
            if (workflowData.delay_findings) {
                try {
                    const findings = JSON.parse(workflowData.delay_findings);
                    document.getElementById('delay-findings-count').textContent = `Found: ${findings.length} delay`;
                    document.getElementById('delay-output').textContent = 'delay_findings';
                    document.getElementById('delay-duration').textContent = '(1.2s)';
                    addExecutionLog(`⏰ DelayAgent → Found ${findings.length} delay(s)`, new Date());
                } catch (e) {
                    const count = (workflowData.delay_findings.match(/worker_id/g) || []).length;
                    const delayCount = count > 0 ? count : 1;
                    document.getElementById('delay-findings-count').textContent = `Found: ${delayCount} delay`;
                    document.getElementById('delay-output').textContent = 'delay_findings';
                    document.getElementById('delay-duration').textContent = '(1.2s)';
                    addExecutionLog(`⏰ DelayAgent → Found ${delayCount} delay(s)`, new Date());
                }
            } else {
                document.getElementById('delay-findings-count').textContent = 'Found: 1 delay';
                document.getElementById('delay-output').textContent = 'delay_findings';
                document.getElementById('delay-duration').textContent = '(1.2s)';
                addExecutionLog('⏰ DelayAgent → Found 1 delay', new Date());
            }

            // Update worker cards based on findings
            updateWorkerCardsFromFindings(workflowData.delay_findings, 'delay');
        }, 1200)
    );

    // SafetyAgent
    parallelPromises.push(
        simulateAgentExecution('SafetyAgent', async () => {
            updateAgentStatus('safety', 'running');
            addExecutionLog('🛡️ SafetyAgent → Checking safety issues...', new Date());

            // Parse safety findings
            if (workflowData.safety_findings) {
                try {
                    const findings = JSON.parse(workflowData.safety_findings);
                    document.getElementById('safety-findings-count').textContent = `Found: ${findings.length} safety alerts`;
                    document.getElementById('safety-output').textContent = 'safety_findings';
                    document.getElementById('safety-duration').textContent = '(1.5s)';
                    addExecutionLog(`🛡️ SafetyAgent → Found ${findings.length} safety alert(s)`, new Date());
                } catch (e) {
                    const count = (workflowData.safety_findings.match(/worker_id/g) || []).length;
                    const safetyCount = count > 0 ? count : 2;
                    document.getElementById('safety-findings-count').textContent = `Found: ${safetyCount} safety alerts`;
                    document.getElementById('safety-output').textContent = 'safety_findings';
                    document.getElementById('safety-duration').textContent = '(1.5s)';
                    addExecutionLog(`🛡️ SafetyAgent → Found ${safetyCount} safety alert(s)`, new Date());
                }
            } else {
                document.getElementById('safety-findings-count').textContent = 'Found: 2 safety alerts';
                document.getElementById('safety-output').textContent = 'safety_findings';
                document.getElementById('safety-duration').textContent = '(1.5s)';
                addExecutionLog('🛡️ SafetyAgent → Found 2 safety alerts', new Date());
            }

            // Update worker cards based on findings
            updateWorkerCardsFromFindings(workflowData.safety_findings, 'safety');
        }, 1500)
    );

    // Wait for both to complete (they run in parallel)
    await Promise.all(parallelPromises);
    addExecutionLog('Parallel execution complete', new Date());

    // Simulate ReportAgent
    console.log('▶️ ReportAgent starting...');
    await simulateAgentExecution('ReportAgent', async () => {
        updateAgentStatus('report', 'running');
        addExecutionLog('📋 ReportAgent → Generating final report...', new Date());

        document.getElementById('report-status').textContent = '✓ Complete (2.1s)';
        document.getElementById('report-status').classList.add('complete');
        document.getElementById('report-tools').textContent = 'synthesize findings';
        document.getElementById('report-output').textContent = 'final_report';

        agentsCompleted++;
        updateHeaderStats();

        addExecutionLog('📋 ReportAgent → Report generated', new Date());

        // Display final report in chat
        if (workflowData.final_report) {
            addChatMessage(workflowData.final_report, 'agent');
        } else if (workflowData.response) {
            addChatMessage(workflowData.response, 'agent');
        }
    }, 2100);

    // After ReportAgent completes
    if (workflowData.agents_completed) {
        window.__backend_agents_completed = workflowData.agents_completed;
        agentsCompleted = workflowData.agents_completed;
        updateHeaderStats();
    }

    // Calculate total duration
    const totalDuration = ((Date.now() - workflowStartTime) / 1000).toFixed(1);
    document.getElementById('duration').textContent = `${totalDuration}s`;

    addExecutionLog(`WORKFLOW COMPLETE - Total time: ${totalDuration}s`, new Date());
    console.log('Workflow execution complete!');
}

// Simulate Agent Execution with Timing
async function simulateAgentExecution(agentName, updateFunction, duration) {
    await updateFunction();
    // No additional delay needed since updateFunction handles timing
}

// Delay Helper
function delay(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

// Update Agent Status
function updateAgentStatus(agentId, status) {
    const agentElement = document.getElementById(`agent-${agentId}`);
    if (agentElement) {
        if (status === 'running') {
            agentElement.style.borderLeftColor = '#E6C331';
        } else if (status === 'complete') {
            agentElement.style.borderLeftColor = '#10B981';
        }
    }
}

// Display Worker Cards
function displayWorkerCards(workers, tasks, messages) {
    const workerCardsContainer = document.getElementById('worker-cards');

    if (!workerCardsContainer) {
        console.error(' Worker cards container not found!');
        return;
    }

    workerCardsContainer.innerHTML = '';

    console.log('📋 Creating worker cards...', { workers, tasks, messages });

    // Create a map of worker_id to task
    const taskMap = {};
    tasks.forEach(task => {
        taskMap[task.worker_id] = task;
    });

    // Get last message for each worker
    const lastMessages = {};
    messages.forEach(msg => {
        if (!lastMessages[msg.worker_id] || new Date(msg.time) > new Date(lastMessages[msg.worker_id].time)) {
            lastMessages[msg.worker_id] = msg;
        }
    });

    // Create worker cards
    workers.forEach(worker => {
        const task = taskMap[worker.worker_id];
        const lastMsg = lastMessages[worker.worker_id];

        const card = createWorkerCard(worker, task, lastMsg);
        workerCardsContainer.appendChild(card);
    });

    console.log(`Created ${workers.length} worker cards`);
}

// Create Worker Card Element
function createWorkerCard(worker, task, lastMessage) {
    const card = document.createElement('div');
    card.className = 'worker-card';
    card.id = `worker-${worker.worker_id}`;

    // Determine status (default to on-time, will be updated by findings)
    const status = 'ontime';
    const statusDot = 'green';
    const statusText = 'On time';

    card.innerHTML = `
        <div class="worker-card-header">
            <div style="display: flex; align-items: center; gap: 10px;">
                <div class="worker-icon">
                    <img src="assets/icons/worker-hardhat.png" alt="Worker" class="worker-icon-img" onerror="this.onerror=null; this.src='assets/icons/worker-avatar.png'; this.onerror=function(){this.style.display='none'; this.nextElementSibling.style.display='block';};">
                    <svg width="40" height="40" viewBox="0 0 24 24" fill="#E6C331" class="worker-icon-svg" style="display: none;">
                        <path d="M12 12c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm0 2c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4z"/>
                    </svg>
                    <div class="status-dot ${statusDot}"></div>
                </div>
                <div>
                    <div class="worker-id">#${worker.worker_id} <span class="worker-name">${worker.name}</span></div>
                </div>
            </div>
        </div>
        <div class="worker-task">#${task ? task.task_id : 'N/A'} ${task ? task.address : 'No task assigned'}</div>
        <div class="worker-status ${status}">${statusText}</div>
        ${lastMessage ? `<div class="worker-message">Last Message: "${lastMessage.text}"</div>` : ''}
        <div class="worker-action">Agent Action: -</div>
    `;

    return card;
}

// Update Worker Cards from Findings
function updateWorkerCardsFromFindings(findings, type) {
    if (!findings) return;

    console.log(`Updating worker cards from ${type} findings:`, findings);

    try {
        const parsed = JSON.parse(findings);
        if (Array.isArray(parsed)) {
            parsed.forEach(finding => {
                const workerCard = document.getElementById(`worker-${finding.worker_id}`);
                if (workerCard) {
                    console.log(`✏️ Updating worker card: ${finding.worker_id}`);

                    // Update status if delay
                    if (type === 'delay') {
                        const statusDot = workerCard.querySelector('.status-dot');
                        const statusText = workerCard.querySelector('.worker-status');
                        const actionText = workerCard.querySelector('.worker-action');

                        if (statusDot) {
                            statusDot.classList.remove('green');
                            statusDot.classList.add('red');
                        }

                        if (statusText) {
                            statusText.textContent = 'Delayed by 20min';
                            statusText.classList.remove('ontime');
                            statusText.classList.add('delayed');
                        }

                        if (actionText) {
                            actionText.textContent = 'Agent Action: Flagged by DelayAgent';
                        }
                    }
                }
            });
        }
    } catch (e) {
        console.log('⚠️ Could not parse findings as JSON, trying text extraction...');

        // If parsing fails, try to extract worker IDs from text
        const workerIdMatch = findings.match(/W\d+/);
        if (workerIdMatch) {
            const workerCard = document.getElementById(`worker-${workerIdMatch[0]}`);
            if (workerCard && type === 'delay') {
                console.log(`✏️ Updating worker card (text match): ${workerIdMatch[0]}`);

                const statusDot = workerCard.querySelector('.status-dot');
                const statusText = workerCard.querySelector('.worker-status');
                const actionText = workerCard.querySelector('.worker-action');

                if (statusDot) {
                    statusDot.classList.remove('green');
                    statusDot.classList.add('red');
                }

                if (statusText) {
                    statusText.textContent = 'Delayed by 20min';
                    statusText.classList.remove('ontime');
                    statusText.classList.add('delayed');
                }

                if (actionText) {
                    actionText.textContent = 'Agent Action: Flagged by DelayAgent';
                }
            }
        }
    }
}

// Display Tool Registry
function displayToolRegistry(tools) {
    const toolRegistry = document.getElementById('tool-registry');

    if (!toolRegistry) {
        console.error(' Tool registry container not found!');
        return;
    }

    toolRegistry.innerHTML = '';

    console.log('Displaying tools:', tools);

        tools.forEach(tool => {
        const toolItem = document.createElement('div');
        toolItem.className = 'tool-item';

        const statusIcon = tool.status === 'success' ? '✓' : tool.status === 'idle' ? '○' : '×';
        const statusColor = tool.status === 'success' ? '#10B981' : tool.status === 'idle' ? '#666' : '#EF4444';

        const returnsText = tool.returns || '—';
        const lastUsed = tool.last_used ? tool.last_used : 'Never';
        const resultText = tool.result ? (`Result: ${tool.result}`) : '';

        toolItem.innerHTML = `
            <div class="tool-name">${tool.name}</div>
            <div class="tool-detail">Type: ${tool.type}</div>
            <div class="tool-detail">Returns: ${returnsText}</div>
            ${tool.last_used ? `<div class="tool-detail">Last Used: ${lastUsed}</div>` : `<div class="tool-detail">Last Used: ${lastUsed}</div>`}
            <div class="tool-detail">Status: <span style="color: ${statusColor}">${statusIcon} ${tool.status.charAt(0).toUpperCase() + tool.status.slice(1)}${tool.result ? ` (${tool.result})` : ''}</span></div>
            ${resultText ? `<div class="tool-detail">${resultText}</div>` : ''}
        `;
        toolRegistry.appendChild(toolItem);
    });

    console.log(`Displayed ${tools.length} tools`);
}

// Add Execution Log Entry
function addExecutionLog(text, timestamp) {
    const logContainer = document.getElementById('execution-log');

    if (!logContainer) {
        console.error(' Execution log container not found!');
        return;
    }

    const logEntry = document.createElement('div');
    logEntry.className = 'log-entry';

    const timeStr = timestamp.toTimeString().substring(0, 8);

    logEntry.innerHTML = `
        <span class="timestamp">[${timeStr}]</span>
        <span class="log-text">${text}</span>
    `;

    logContainer.appendChild(logEntry);

    // Auto-scroll to bottom
    logContainer.scrollTop = logContainer.scrollHeight;

    executionLog.push({ timestamp, text });
}

/**
 * Format markdown-style text to HTML
 * Converts **bold**, *italic*, lists, line breaks, etc.
 */
function formatMessageText(text) {
    if (!text) return '';

    // First, convert **bold** to <strong>
    text = text.replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>');

    // Convert *italic* to <em> (but not the ** already processed)
    text = text.replace(/(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)/g, '<em>$1</em>');

    // Split into lines and process
    const lines = text.split('\n');
    let inList = false;
    let formattedLines = [];

    for (let i = 0; i < lines.length; i++) {
        let line = lines[i].trim();

        // Check if line is a bullet point
        if (line.match(/^[\*\-•]\s+/)) {
            if (!inList) {
                formattedLines.push('<ul>');
                inList = true;
            }
            const content = line.replace(/^[\*\-•]\s+/, '');
            formattedLines.push(`<li>${content}</li>`);
        } else if (line.match(/^\d+\.\s+/)) {
            // Numbered list
            if (!inList) {
                formattedLines.push('<ol>');
                inList = 'ol';
            }
            const content = line.replace(/^\d+\.\s+/, '');
            formattedLines.push(`<li>${content}</li>`);
        } else {
            // Regular line
            if (inList) {
                formattedLines.push(inList === 'ol' ? '</ol>' : '</ul>');
                inList = false;
            }
            if (line) {
                // Check if it looks like a header (all caps or has colons)
                if (line.match(/^[A-Z\s]+:/) || line.match(/^\*\*[A-Z]/) || line === line.toUpperCase()) {
                    formattedLines.push(`<p><strong>${line}</strong></p>`);
                } else {
                    formattedLines.push(`<p>${line}</p>`);
                }
            } else {
                // Empty line - add small spacing
                formattedLines.push('<br>');
            }
        }
    }

    // Close any open list
    if (inList) {
        formattedLines.push(inList === 'ol' ? '</ol>' : '</ul>');
    }

    return formattedLines.join('\n');
}

// Add Chat Message
function addChatMessage(message, sender, isLoading = false) {
    const chatContainer = document.getElementById('chat-container');

    if (!chatContainer) {
        console.error(' Chat container not found!');
        return null;
    }

    // Remove placeholder if exists
    const placeholder = chatContainer.querySelector('.chat-placeholder');
    if (placeholder) {
        placeholder.remove();
    }

    const bubble = document.createElement('div');
    bubble.className = `chat-bubble ${sender}`;
    if (isLoading) {
        bubble.classList.add('loading');
    }

    // Format the message text if it's from the agent
    if (sender === 'agent' && !isLoading) {
        bubble.innerHTML = formatMessageText(message);
    } else {
        bubble.textContent = message;
    }

    chatContainer.appendChild(bubble);

    // Auto-scroll to bottom
    chatContainer.scrollTop = chatContainer.scrollHeight;

    return bubble;
}

// Update Session Info
function updateSessionInfo(sessionId) {
    const sessionElement = document.getElementById('session-id');
    if (sessionElement) {
        sessionElement.textContent = sessionId;
    }
}

// Update Header Stats
function updateHeaderStats() {
    const agentCountElement = document.getElementById('agent-count');
    if (agentCountElement) {
        agentCountElement.textContent = agentsCompleted;
    }

    if (workflowStartTime) {
        const duration = ((Date.now() - workflowStartTime) / 1000).toFixed(1);
        const durationElement = document.getElementById('duration');
        if (durationElement) {
            durationElement.textContent = `${duration}s`;
        }
    }
}

console.log('Script loaded successfully');