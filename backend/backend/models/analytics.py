from typing import Dict, List, Optional, Union
from pydantic import BaseModel, Field
from datetime import datetime

class DeviceInfo(BaseModel):
    screenSize: str
    viewport: str
    devicePixelRatio: float
    platform: str

class FormView(BaseModel):
    form_type: str
    timestamp: datetime = Field(default_factory=datetime.now)
    referrer: Optional[str]
    userAgent: str
    deviceInfo: DeviceInfo

class FormStart(BaseModel):
    form_type: str
    timestamp: datetime = Field(default_factory=datetime.now)
    session_id: str
    userAgent: str
    screenSize: Dict[str, int]
    previousAttempts: List[Dict[str, Union[str, datetime]]] = []

class CompletionPath(BaseModel):
    field_name: str
    timestamp: datetime
    is_valid: bool
    time_spent: float

class FormCompletion(BaseModel):
    form_type: str
    session_id: str
    timestamp: datetime = Field(default_factory=datetime.now)
    completion_time: float
    completion_path: List[CompletionPath]
    field_completion_rates: Dict[str, float]
    validation_attempts: Dict[str, int]
    completed: bool = True

class FormAbandonment(BaseModel):
    form_type: str
    session_id: str
    timestamp: datetime = Field(default_factory=datetime.now)
    last_step: int
    completion_percentage: float
    time_spent: float
    last_interaction: Dict[str, Union[str, datetime]]
    abandonment_reason: Dict[str, str]
    incomplete_fields: List[str]
    form_progress: Dict[str, Union[bool, float]]
    abandoned: bool = True

class ValidationError(BaseModel):
    field: str
    error_type: str
    message: str

class FieldInteraction(BaseModel):
    form_type: str
    session_id: str
    field_name: str
    timestamp: datetime = Field(default_factory=datetime.now)
    interaction_type: str
    value_length: Optional[int]
    is_valid: bool
    validation_errors: List[ValidationError] = []
    time_spent: float

class FieldTiming(BaseModel):
    form_type: str
    session_id: str
    field_name: str
    timestamp: datetime = Field(default_factory=datetime.now)
    duration: float
    interaction_count: int
    validation_attempts: int

class FormError(BaseModel):
    form_type: str
    session_id: str
    timestamp: datetime = Field(default_factory=datetime.now)
    error_type: str
    error_details: str
    stack_trace: Optional[str]
    current_step: int
    form_state: Dict[str, Any]
    browser_info: Dict[str, str]

class FieldAnalytics(BaseModel):
    total_interactions: int
    validation_success_rate: float
    avg_attempts: float
    avg_time_spent: float
    common_errors: List[str]

class FormAnalytics(BaseModel):
    total_views: int
    total_starts: int
    total_completions: int
    total_abandonments: int
    avg_completion_time: float
    field_completion_rates: Dict[str, float]
    active_sessions: int
    recent_completions: int
    recent_paths: List[str]

class AbandonmentAnalysis(BaseModel):
    reason_type: str
    count: int
    avg_completion_percentage: float
    common_last_fields: List[str]
    avg_time_spent: float

class FormSuccessRate(BaseModel):
    total_attempts: int
    successful_submissions: int
    success_rate: float
    avg_attempts_before_success: float
    completion_time_distribution: List[float]
    real_time_success_rate: float 