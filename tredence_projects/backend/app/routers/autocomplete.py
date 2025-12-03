from fastapi import APIRouter
from ..schemas import AutocompleteReq, AutocompleteResp

router = APIRouter()

@router.post('/autocomplete', response_model=AutocompleteResp)
async def autocomplete(req: AutocompleteReq):
    code = req.code or ''
    suggestion = ''
    trimmed = code.rstrip()
    if trimmed.endswith('def') or trimmed.endswith('def '):
        suggestion = 'def function_name(args):\n    """describe\n    """\n    pass'
    elif trimmed.endswith('for') or trimmed.endswith('for '):
        suggestion = 'for i in range(n):\n    pass'
    elif 'import ' in trimmed.splitlines()[-1]:
        suggestion = 'import os\n# os functions...'
    else:
        if trimmed.endswith('TODO'):
            suggestion = '# TODO: implement this'
        else:
            suggestion = '# suggestion: try adding a function or loop'

    return {'suggestion': suggestion}
