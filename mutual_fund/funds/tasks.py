import logging
from .models import MutualFundFamily, MutualFundScheme
from .services import MutualFundService

logger = logging.getLogger(__name__)

def update_mutual_fund_schemes():
    fund_families = MutualFundFamily.objects.all()
    for fund_family in fund_families:
        data = MutualFundService.fetch_open_ended_schemes_for_family(fund_family.mutual_fund_family)
        if data.get("success"):
            result = MutualFundService.save_schemes_to_db(fund_family, data)
            if result.get("success"):
                logger.info(f"Successfully updated schemes for {fund_family.mutual_fund_family}")
            else:
                logger.error(f"Failed to save schemes: {data.get('error', 'Unknown error')}")
        else:
            logger.error(f"Failed to fetch schemes: {data.get('error', 'Unknown error')}")
