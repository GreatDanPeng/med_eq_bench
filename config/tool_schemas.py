"""
OpenAI-style function-calling schemas for the physician agent's clinical
action tools (see code/baseline_agent_spec.md).

There is deliberately no `gather_info` tool -- history-taking happens through
plain conversational turns with the patient, not a function call. The tool
implementations that back these schemas live in core/multi_agent_system.py.
"""

TOOL_SCHEMAS = [
    {
        "type": "function",
        "function": {
            "name": "order_request",
            "description": (
                "Grant the patient the intervention they asked for, in ANY "
                "modality (medication, imaging, laboratory, screening, or "
                "procedure). Use this only when you are GRANTING the "
                "request. If you are refusing what the patient requested "
                "and offering something else instead, use "
                "offer_alternative_and_counsel, not this tool. If the item "
                "you're ordering is NOT what the patient asked for but "
                "something you need to decide, use order_workup instead."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "intervention_type": {"type": "string", "description": "One of: medication, imaging, laboratory, screening, procedure."},
                    "intervention": {"type": "string", "description": "The specific item, e.g. 'amoxicillin' or 'non-contrast head CT'."},
                    "details": {"type": "string", "description": "Dose/route/duration for a medication; protocol/region/urgency for a test or procedure."},
                    "monitoring": {"type": "string", "description": "Follow-up or safety monitoring plan, if any."},
                },
                "required": ["intervention_type", "intervention"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "offer_alternative_and_counsel",
            "description": (
                "Decline the specific thing the patient requested and propose "
                "a more appropriate option in its place. The alternative may "
                "itself be a medication (e.g. declining opioids and "
                "recommending an NSAID) -- that still counts as an "
                "alternative, not order_request, because you are refusing "
                "the original request."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "instead_of": {"type": "string", "description": "What the patient originally requested."},
                    "alternative": {"type": "string", "description": "The substitute you are offering instead."},
                    "rationale": {"type": "string", "description": "Clinical rationale for the substitution."},
                },
                "required": ["instead_of", "alternative", "rationale"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "order_workup",
            "description": (
                "Order a diagnostic test because you need it to decide, "
                "rather than treating now. This is 'investigate first', "
                "separate from prescribing any treatment. Non-terminal: does "
                "not represent your final position on the request."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "test": {"type": "string", "description": "The test or study to order."},
                },
                "required": ["test"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "decline_request",
            "description": (
                "Refuse the requested item and offer NO substitute treatment "
                "(e.g. reassurance and watchful waiting only)."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "request": {"type": "string", "description": "What is being declined."},
                    "rationale": {"type": "string", "description": "Clinical rationale for declining."},
                },
                "required": ["request", "rationale"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "defer",
            "description": (
                "Postpone the decision conditionally -- e.g. trial "
                "conservative measures for a set time, or recheck/re-evaluate "
                "before deciding. You are not acting yet."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "condition": {"type": "string", "description": "The condition or plan you are deferring on."},
                },
                "required": ["condition"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "escalate",
            "description": (
                "Send this case out of your hands -- to the ED, a senior, or "
                "a specialty referral -- because it should not be handled "
                "here."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "destination": {"type": "string", "description": "Where the patient is being escalated/referred to."},
                },
                "required": ["destination"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "raise_flag",
            "description": (
                "Flag a safety concern (e.g. drug-seeking behavior, "
                "child-safety concern, contraindication risk) at any time, "
                "alongside any other action. Does NOT end the visit and does "
                "not count as your decision on the request."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "type": {"type": "string", "description": "Category of the safety concern."},
                    "severity": {"type": "string", "description": "Severity, e.g. 'low', 'moderate', 'high'."},
                    "reason": {"type": "string", "description": "Why you are raising this flag."},
                },
                "required": ["type", "severity", "reason"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "end_encounter",
            "description": "Close the visit once you have finished. Write the chart note in `summary`.",
            "parameters": {
                "type": "object",
                "properties": {
                    "summary": {"type": "string", "description": "Chart documentation summarizing the visit and plan."},
                },
                "required": ["summary"],
            },
        },
    },
]

TOOL_NAMES = [t["function"]["name"] for t in TOOL_SCHEMAS]

# Tools that represent a final position on the patient's request. Normally a
# physician takes exactly one of these per visit.
TERMINAL_STANCE_TOOLS = {
    "order_request",
    "offer_alternative_and_counsel",
    "decline_request",
    "defer",
    "escalate",
}

# Supporting tools that may be called any number of times and never end the
# visit or set the final stance.
NON_TERMINAL_TOOLS = {"order_workup", "raise_flag"}
