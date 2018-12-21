from rest_framework import renderers
from rest_framework.compat import (
    INDENT_SEPARATORS, LONG_SEPARATORS, SHORT_SEPARATORS, coreapi,
    pygments_css
)
from django.utils import six
import json

code_dic = {401: u'用户未登录', 405: u'不被支持的操作类型',20000: u'Sucess'} # 注意4xx,5xx的错误

class APIRenderer(renderers.JSONRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        status_code = renderer_context['response'].status_code
        if data is None:
            data = {}
        data = {'code': 20000, 'data': data}
        if status_code in code_dic.keys():
            data = {
                'code': status_code,
                'message': code_dic[status_code],
            }
        renderer_context = renderer_context or {}
        indent = self.get_indent(accepted_media_type, renderer_context)

        if indent is None:
            separators = SHORT_SEPARATORS if self.compact else LONG_SEPARATORS
        else:
            separators = INDENT_SEPARATORS

        ret = json.dumps(
            data, cls=self.encoder_class,
            indent=indent, ensure_ascii=self.ensure_ascii,
            allow_nan=not self.strict, separators=separators
        )

        if isinstance(ret, six.text_type):
            # We always fully escape \u2028 and \u2029 to ensure we output JSON
            # that is a strict javascript subset. If bytes were returned
            # by json.dumps() then we don't have these characters in any case.
            # See: http://timelessrepo.com/json-isnt-a-javascript-subset
            ret = ret.replace('\u2028', '\\u2028').replace('\u2029', '\\u2029')
            return bytes(ret.encode('utf-8'))
        return ret