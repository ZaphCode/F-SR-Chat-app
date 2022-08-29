from fastapi.responses import RedirectResponse
from routers.views_router import j2

#* HANDLERS
async def requeries_login_exc_handler(request, exc):
    return RedirectResponse('/signin', 307)
    
async def not_found_exc_handler(request, exc):
    return j2.TemplateResponse('not_found.html', {"request": request})

async def internal_err_handler(request, exc):
    return j2.TemplateResponse('error.html', {
            "request": request, "error_type": "INTERNAL_SERVER_ERR",
            "error_msg": "Catastropical error", "error_code": 500
        }
    )

async def server_error_page_exc_handler(request, exc):
    return j2.TemplateResponse('error.html', {
            "request": request, "error_type": exc.error_type,
            "error_msg": exc.error_msg, "error_code": exc.error_code
        }
    )
