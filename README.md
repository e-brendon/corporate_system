# Corporate System

**Estrutura tem que ficar assim:**

```python
CorporateSystem/
├── apps/
│   ├── **base**/
│   │   ├── migrations/
│   │   ├── **static**/
│   │   │   ├── **css**/
│   │   │   ├── **js**/
│   │   │   ├── **fonts**/
│   │   │   └── **images**/
│   │   ├── **templates**/
│   │   └── __init__.py 
├── core/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   ├── **context_processors.py**
│   └── wsgi.py
├── manage.py
└── requirements.txt
```
