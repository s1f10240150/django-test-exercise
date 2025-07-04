from django.shortcuts import render, redirect
from django.utils import timezone
from datetime import datetime
from .models import Task

def index(request):
    """
    タスクの一覧を表示し、新しいタスクの作成を処理するビュー。
    forms.py を使用せず、直接 request.POST からデータを処理します。
    """
    if request.method == 'POST':
        # POST リクエストの場合、フォームデータを直接処理
        title = request.POST.get('title')
        due_at_str = request.POST.get('due_at')

        # due_at が提供された場合、文字列を datetime オブジェクトに変換
        due_at = None
        if due_at_str:
            try:
                # テストで送られる形式 'YYYY-MM-DD HH:MM:SS' に対応
                due_at = timezone.make_aware(datetime.strptime(due_at_str, '%Y-%m-%d %H:%M:%S'))
            except ValueError:
                # 日付形式が不正な場合のエラーハンドリング (ここでは単純に None に設定)
                pass

        if title: # タイトルが空でないことを確認
            # Task モデルのインスタンスを作成し、保存
            Task.objects.create(title=title, due_at=due_at)
            # タスク保存後、同じページにリダイレクトして「Post/Redirect/Get」パターンを実装
            return redirect('index')
        # タイトルが空の場合や、その他のバリデーションエラーの場合、
        # ここでエラーメッセージをコンテキストに追加して再レンダリングすることも可能ですが、
        # 今回はシンプルにリダイレクトなしで再表示します。

    # GET リクエストの場合、または POST でタスク作成に失敗した場合
    # タスクの並べ替えロジック
    order = request.GET.get('order', 'post') # デフォルトは 'post' (作成日時順)

    if order == 'due':
        # 期日 (due_at) の昇順でタスクを取得
        tasks = Task.objects.all().order_by('due_at')
    elif order == 'post':
        # 作成日時 (posted_at) の昇順でタスクを取得
        tasks = Task.objects.all().order_by('posted_at')
    else:
        # その他の場合は、デフォルトの並び順（通常は id 順）
        tasks = Task.objects.all()

    # テンプレートに渡すコンテキストデータ
    context = {
        'tasks': tasks,
        # forms.py を使わないため、form オブジェクトは不要
    }
    # 'todo/index.html' テンプレートをレンダリングして応答
    return render(request, 'todo/index.html', context)
