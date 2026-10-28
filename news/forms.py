from django import forms
from django.db.models import Q

from accounts.models import User

from .access import articles_for_newsletter
from .models import Article, Newsletter, Publication


class ArticleForm(forms.ModelForm):
    """
    The form for writing a new article or editing one.

    A new article can be independent or for a publication its author is
    on the staff of. Once the article exists, its publication cannot
    change.
    """

    class Meta:
        model = Article
        fields = ["title", "content", "publication"]
        widgets = {
            "content": forms.Textarea(attrs={"rows": 16}),
        }

    def __init__(self, *args, author, **kwargs):
        """
        Builds the form for the article's author, offering only the
        publications they are on the staff of.
        """
        super().__init__(*args, **kwargs)

        # An existing article keeps its publication, so the edit form
        # has no publication field. The page shows the publication as
        # text.
        if self.instance.pk is not None:
            del self.fields["publication"]
            return

        publication_field = self.fields["publication"]

        # The empty choice means an independent article.
        publication_field.empty_label = "Independent"
        publication_field.queryset = author.journalist_publications.order_by(
            "name"
        )
        publication_field.help_text = (
            "You approve your own independent articles. A "
            "publication's editors approve its articles."
        )


class NewsletterForm(forms.ModelForm):
    """
    The form for putting together a new newsletter or editing one.

    A new newsletter can be independent or for a publication its author
    is on the staff of. Once the newsletter exists, its publication
    cannot change.

    An independent newsletter can include only its author's approved
    independent articles. A publication's newsletter can include only
    that publication's approved articles.
    """

    class Meta:
        model = Newsletter
        fields = ["title", "description", "publication", "articles"]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 4}),
            "articles": forms.CheckboxSelectMultiple,
        }

    def __init__(self, *args, author, **kwargs):
        """
        Builds the form for the newsletter's author, offering only the
        publications and articles they may use.
        """
        super().__init__(*args, **kwargs)
        self.author = author

        articles_field = self.fields["articles"]

        if self.instance.pk is not None:
            # An existing newsletter keeps its publication, so the edit
            # form has no publication field, and the page shows it as
            # text. Only the articles that fit it are offered.
            del self.fields["publication"]
            articles_field.queryset = articles_for_newsletter(
                author, self.instance.publication
            ).select_related("author", "publication")
        else:
            # The empty choice means an independent newsletter.
            publication_field = self.fields["publication"]
            publication_field.queryset = (
                author.journalist_publications.order_by("name")
            )
            publication_field.empty_label = "Independent"

            # Every article the author could use in any of their
            # newsletters. The check in clean() makes sure the chosen
            # ones fit the chosen publication.
            articles_field.queryset = (
                Article.objects.filter(approved=True)
                .filter(
                    Q(author=author, publication__isnull=True)
                    | Q(publication__in=publication_field.queryset)
                )
                .select_related("author", "publication")
            )

        articles_field.label_from_instance = self.article_label

    @staticmethod
    def article_label(article):
        """
        The label beside an article's checkbox: its title, author, and
        publication.
        """
        if article.publication:
            where = article.publication.name
        else:
            where = "Independent"
        return f"{article.title} (by {article.author}, {where})"

    def clean(self):
        """
        Checks that every chosen article fits the newsletter's
        publication, and names the ones that do not.
        """
        cleaned_data = super().clean()
        articles = cleaned_data.get("articles")

        # On the edit form there is no publication field, so the
        # newsletter's own publication is used.
        publication = cleaned_data.get(
            "publication", self.instance.publication
        )

        # Missing when the articles already failed their own checks.
        if articles:
            allowed_ids = set(
                articles_for_newsletter(self.author, publication)
                .filter(pk__in=[article.pk for article in articles])
                .values_list("pk", flat=True)
            )
            misfits = [
                article.title
                for article in articles
                if article.pk not in allowed_ids
            ]

            if misfits:
                if publication:
                    where = publication.name
                else:
                    where = "an independent newsletter"
                self.add_error(
                    "articles",
                    f"These articles do not belong in {where}: "
                    + "; ".join(misfits)
                    + ".",
                )

        return cleaned_data


class PublicationForm(forms.ModelForm):
    """
    The form for creating a publication or editing one, including
    choosing its editors and journalists.
    """

    class Meta:
        model = Publication
        fields = ["name", "description", "editors", "journalists"]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 4}),
            "editors": forms.CheckboxSelectMultiple,
            "journalists": forms.CheckboxSelectMultiple,
        }

    def __init__(self, *args, **kwargs):
        """
        Builds the form, offering every editor and journalist as staff,
        by username.
        """
        super().__init__(*args, **kwargs)

        self.fields["editors"].queryset = User.objects.filter(
            role=User.EDITOR
        ).order_by("username")
        self.fields["journalists"].queryset = User.objects.filter(
            role=User.JOURNALIST
        ).order_by("username")

        self.fields["editors"].help_text = (
            "Editors approve, edit, and delete this publication's "
            "articles and newsletters."
        )
        self.fields["journalists"].help_text = (
            "Journalists write, edit, and delete this publication's "
            "articles and newsletters."
        )
