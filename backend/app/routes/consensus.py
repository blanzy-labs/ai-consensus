from fastapi import APIRouter, Depends, HTTPException, status

from app.config import Settings, get_settings
from app.llm.base import (
    MissingProviderConfigError,
    ProviderError,
    ProviderRequestError,
    UnsupportedProviderError,
)
from app.schemas import ConsensusRequest, ConsensusResponse
from app.services.consensus_service import ConsensusService

router = APIRouter(prefix="/consensus", tags=["consensus"])


def get_consensus_service(settings: Settings = Depends(get_settings)) -> ConsensusService:
    return ConsensusService(settings=settings)


@router.post("/run", response_model=ConsensusResponse)
def run_consensus(
    request: ConsensusRequest,
    service: ConsensusService = Depends(get_consensus_service),
) -> ConsensusResponse:
    try:
        return service.run(request)
    except UnsupportedProviderError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc
    except MissingProviderConfigError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc
    except ProviderRequestError as exc:
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail=str(exc)) from exc
    except ProviderError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc
