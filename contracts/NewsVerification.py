# v0.2.16
# { "Depends": "py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6" }
from genlayer import *
import json

class NewsVerifier(gl.Contract):
    has_verified: bool
    article_url: str
    article_title: str
    overall_verdict: str
    overall_confidence: u256
    summary: str
    claims_json: str

    def __init__(self):
        self.has_verified=False
        self.article_url=""
        self.article_title=""
        self.overall_verdict=""
        self.overall_confidence=u256(0)
        self.summary=""
        self.claims_json="[]"

    @gl.public.write
    def verify(self, url:str):
        if self.has_verified:
            raise gl.vm.UserError("Already verified")
        def perform_verification():
            web_data=gl.nondet.web.render(url,mode="text")
            task=f"""Analyze article and return ONLY JSON:
{{"title":"","overall_verdict":"","overall_confidence":0,"summary":"","claims":[{{"claim":"","verdict":"","confidence":0,"reason":""}}]}}
ARTICLE:{web_data}"""
            return json.loads(gl.nondet.exec_prompt(task).replace("```json","").replace("```",""))
        result=gl.eq_principle.strict_eq(perform_verification)
        self.has_verified=True
        self.article_url=url
        self.article_title=str(result.get("title","Unknown"))
        self.overall_verdict=str(result.get("overall_verdict","Unverifiable"))
        self.overall_confidence=u256(int(result.get("overall_confidence",0)))
        self.summary=str(result.get("summary",""))
        self.claims_json=json.dumps(result.get("claims",[]))
        return {"verified":True,"verdict":self.overall_verdict}

    @gl.public.view
    def get_result(self):
        return {
            "verified":self.has_verified,
            "article_url":self.article_url,
            "article_title":self.article_title,
            "overall_verdict":self.overall_verdict,
            "overall_confidence":self.overall_confidence,
            "summary":self.summary,
            "claims_json":self.claims_json,
        }
