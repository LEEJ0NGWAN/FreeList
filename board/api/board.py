import json
import datetime
from django.contrib.auth import (
    login, logout
)
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views.generic import View
from rest_framework.status import (
    HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED, HTTP_403_FORBIDDEN,
    HTTP_404_NOT_FOUND, HTTP_409_CONFLICT
)
from board.models import ( Board, Sheet, Node, Edge )
from utils.serialize import serialize

@method_decorator(csrf_exempt, name='dispatch')
class BoardController(View):
    def get(self, request):

        data = request.GET

        if 'id' in data:
            board = Board.objects\
                .filter(
                    id=data['id'],
                    deleted=False).first()

            if not board:
                return JsonResponse({}, status=HTTP_404_NOT_FOUND)
            
            return JsonResponse({
                'board': board
            })
        
        if 'owner_id' in data:
            boards = Board.objects\
                .filter(
                    owner_id=data['owner_id'],
                    deleted=False)\
                .order_by('modify_date').all()
        
        else:
            boards = Board.objects\
                .filter(
                    owner_id=request.user.id,
                    deleted=False)\
                .order_by('modify_date').all()

        return JsonResponse({
            'boards': boards
        })

    def post(self, request):
        if not request.user.is_authenticated:
            return JsonResponse({}, status=HTTP_401_UNAUTHORIZED)
        
        data = json.loads(request.body.decode("utf-8"))

        title = data.get('title')
        
        new_board = Board.objects.create(
            title=title,
            owner_id=request.user.id
        )

        return JsonResponse({
            'board': new_board
        })

    def put(self, request):
        if not request.user.is_authenticated:
            return JsonResponse({}, status=HTTP_401_UNAUTHORIZED)
        
        data = json.loads(request.body.decode("utf-8"))

        if 'id' not in data:
            return JsonResponse({}, status=HTTP_400_BAD_REQUEST)
        
        board = Board.objects\
            .filter(
                id=data.get('id'),
                deleted=False).first()
        
        if not board:
            return JsonResponse({}, status=HTTP_404_NOT_FOUND)
        
        board.title = data.get('title')
        board.save()

        return JsonResponse({
            'board': board
        })

    def delete(self, request):
        if not request.user.is_authenticated:
            return JsonResponse({}, status=HTTP_401_UNAUTHORIZED)
        
        data = request.GET
        
        if 'id' not in data:
            return JsonResponse({}, status=HTTP_400_BAD_REQUEST)
        
        board = Board.objects\
            .filter(
                id=data['id'],
                deleted=False).first()
        
        if not board:
            return JsonResponse({}, status=HTTP_404_NOT_FOUND)
        
        board.deleted = True
        board.save()

        return JsonResponse({
            'board': board
        })

@method_decorator(csrf_exempt, name='dispatch')
class SheetController(View):
    def get(self, request):
        
        data = request.GET

        if 'id' in data:
            sheet = Sheet.objects\
                .filter(
                    id=data['id'],
                    deleted=False).first()
            
            if not sheet:
                return JsonResponse({}, status=HTTP_404_NOT_FOUND)
            
            return JsonResponse({
                'sheet': sheet
            })
        
        if 'board_id' in data:
            sheets = Sheet.objects\
                .filter(
                    board_id=data['board_id'],
                    deleted=False)\
                .order_by('modify_date').all()
        
        else:
            sheets = Sheet.objects\
                .filter(
                    owner_id=request.user.id,
                    deleted=False)\
                .order_by('modify_date').all()
        
        if not sheets:
            return JsonResponse({}, status=HTTP_404_NOT_FOUND)
        
        return JsonResponse({
            'sheets': sheets
        })
        
    def post(self, request):
        if not request.user.is_authenticated:
            return JsonResponse({}, status=HTTP_401_UNAUTHORIZED)
        
        data = json.loads(request.body.decode("utf-8"))

        if 'board_id' not in data:
            return JsonResponse({}, status=HTTP_400_BAD_REQUEST)
        
        new_sheet = Sheet.objects.create(
            title=data.get('title'),
            board_id=data.get('board_id'),
            owner_id=request.user.id
        )

        return JsonResponse({
            'sheet': new_sheet
        })

    def put(self, request):
        if not request.user.is_authenticated:
            return JsonResponse({}, status=HTTP_401_UNAUTHORIZED)
        
        data = json.loads(request.body.decode("utf-8"))

        if 'id' not in data:
            return JsonResponse({}, status=HTTP_400_BAD_REQUEST)
        
        sheet = Sheet.objects\
            .filter(
                id=data.get('id'),
                deleted=False).fisrt()
        
        if not sheet:
            return JsonResponse({}, status=HTTP_404_NOT_FOUND)

        if 'title' in data:
            sheet.title = data.get('title')
        
        if 'board_id' in data:
            sheet.board_id = data.get('board_id')
        
        sheet.save()

        return JsonResponse({
            'sheet': sheet
        })

    def delete(self, request):
        if not request.user.is_authenticated:
            return JsonResponse({}, status=HTTP_401_UNAUTHORIZED)
        
        data = request.GET

        if 'id' not in data:
            return JsonResponse({}, status=HTTP_400_BAD_REQUEST)
        
        sheet = Sheet.objects\
            .filter(
                id=data['id'],
                deleted=False).first()
        
        if not sheet:
            return JsonResponse({}, status=HTTP_404_NOT_FOUND)
        
        sheet.deleted = True
        sheet.save()

        return JsonResponse({
            'sheet': sheet
        })

@method_decorator(csrf_exempt, name='dispatch')
class ElementController(View):
    def get(self, request):
        data = request.GET
        if 'sheet_id' not in data:
            return JsonResponse({}, status=HTTP_400_BAD_REQUEST)
        
        nodes = Node.objects\
            .filter(
                sheet_id=data['sheet_id'],
                deleted=False)\
            .order_by('id').all()
        
        if not nodes:
            return JsonResponse({}, status=HTTP_404_NOT_FOUND)
        
        edges = Edge.objects\
            .filter(
                sheet_id=data['sheet_id'],
                deleted=False)\
            .order_by('id').all()
        
        return JsonResponse({
            'nodes': nodes,
            'edges': edges
        })

    def post(self, request):
        if not request.user.is_authenticated:
            return JsonResponse({}, status=HTTP_401_UNAUTHORIZED)
        
        data = json.loads(request.body.decode("utf-8"))

        if 'sheet_id' not in data \
            or 'nodes' not in data or 'edges' not in data:
            return JsonResponse({}, status=HTTP_400_BAD_REQUEST)

        parse = dict()
        nodes = list()
        edges = list()

        nodes_app = nodes.append
        edges_app = edges.append

        for raw in data['nodes']:
            if 'id' not in raw:
                continue

            nodes_app(Node(
                sheet_id=data['sheet_id'],
                label=raw.get('label')
            ))
        
        nodes = Node.objects.bulk_create(nodes)
        
        index = 0
        for raw in data['nodes']:
            if 'id' not in raw:
                continue
            parse[raw['id']] = nodes[index].id
            index+=1
        
        for raw in data['edges']:
            if 'node1_id' not in raw\
            or 'node2_id' not in raw:
                continue

            edges_app(Edge(
                node1_id=parse[raw['node1_id']],
                node2_id=parse[raw['node2_id']],
                sheet_id=data['sheet_id']
            ))
        
        edges = Edge.objects.bulk_create(edges)

        return JsonResponse({
            'nodes': nodes,
            'edges': edges
        })

    def put(self, request):
        if not request.user.is_authenticated:
            return JsonResponse({}, status=HTTP_401_UNAUTHORIZED)
        
        data = json.loads(request.body.decode("utf-8"))

        nodes = None
        edges = None

        if 'nodes' in data:
            raws = dict()
            nodes = list()
            nodes_app = nodes.append

            for raw in data['nodes']:
                raws[raw['id']] = raw
                nodes_app(raw['id'])
            
            nodes = Node.objects.in_bulk(nodes)

            for pk in nodes:
                if 'label' in raws[pk]:
                    nodes[pk].label = raws[pk]['label']
                if 'deleted' in raws[pk]:
                    nodes[pk].deleted = raws[pk]['deleted']

            nodes = list(nodes.values())
            Node.objects.bulk_update(nodes,['label','deleted'])

        if 'edges' in data:
            raws = dict()
            edges = list()
            edges_app = edges.append

            for raw in data['edges']:
                raws[raw['id']] = raw
                edges_app(raw['id'])
            
            edges = Edge.objects.in_bulk(edges)

            for pk in edges:
                if 'label' in raws[pk]:
                    edges[pk].label = raws[pk]['label']
                if 'node1_id' in raws[pk]:
                    edges[pk].node1_id = raws[pk]['node1_id']
                if 'node2_id' in raws[pk]:
                    edges[pk].node2_id = raws[pk]['node2_id']
                if 'deleted' in raws[pk]:
                    edges[pk].deleted = raws[pk]['deleted']
            
            edges = list(edges.values())
            Edge.objects.bulk_update(
                edges,
                ['label','node1_id','node2_id','deleted'])

        return JsonResponse({
            'nodes': nodes,
            'edges': edges
        })
    
    # TODO: controller 테스트 및 폴리싱
    # TODO: DELETE 메소드 구현?
