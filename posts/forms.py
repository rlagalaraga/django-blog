from django import forms
from posts.models import Post, Comment
from users.models import User

class PostForm(forms.ModelForm):

    title = forms.CharField(max_length=100)
    content = forms.CharField(widget=forms.Textarea)
    picture = forms.ImageField(label='Post Image',widget=forms.FileInput)

    class Meta:
        model = Post
        fields = ['title', 'content', 'picture']

    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        self.fields['picture'].required = False

class UpdatePostForm(forms.ModelForm):

    title = forms.CharField(max_length=100)
    content = forms.CharField(widget=forms.Textarea)
    picture = forms.ImageField(label='Post Image',widget=forms.FileInput)

    class Meta:
        model = Post
        fields = ['title', 'content', 'picture']
    
    def __init__(self, *args, **kwargs):
        super(UpdatePostForm, self).__init__(*args, **kwargs)
        self.fields['picture'].required = False

class CommentForm(forms.ModelForm):
    
    class Meta:
        model = Comment
        fields = ['content']
    
    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        self.fields['content'].required = True

