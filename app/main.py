from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Depends
from app.websocket import websocket_manager
from app.rabbitmq import consume_order_updates
from fastapi.middleware.cors import CORSMiddleware
import threading
import sentry_sdk
from app.config import SENTRY_DSN
origins=["*"]


sentry_sdk.init(
    dsn=SENTRY_DSN,
    # Add data like request headers and IP for users, if applicable;
    # see https://docs.sentry.io/platforms/python/data-management/data-collected/ for more info
    send_default_pii=True,
    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for tracing.
    traces_sample_rate=1.0,
    # Set profiles_sample_rate to 1.0 to profile 100%
    # of sampled transactions.
    # We recommend adjusting this value in production.
    profiles_sample_rate=1.0,
)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.websocket("/ws/{user_id}")
async def websocket_endpoint(user_id: int, websocket: WebSocket):

    await websocket_manager.connect(user_id, websocket)


@app.on_event("startup")
def start_rabbitmq_consumer():
    thread = threading.Thread(target=consume_order_updates, daemon=True)
    thread.start()

@app.get("/")
def root():
    return {"message": "Real-Time Notification Service is running"}
