from typing import List, MutableMapping, Tuple  # noqa
from uqbar.apis.MemberDocumenter import MemberDocumenter
from uqbar.apis.ModuleDocumenter import ModuleDocumenter


class SummarizingModuleDocumenter(ModuleDocumenter):
    """
    A summarizing module documenter.

    Organizes member documenters by their *documentation section*.

    Treats *nominative* submodule documenters (almost) as if they were locally
    defined members. This means that a documenter for a package which contains
    a module which contains *only* one class or function named identically to
    that module will treat that class or function as though it was defined in
    the package's ``__init__.py``. These nominative submodule members are
    organized in each documentation section via an *autosummary* table, rather
    than including their documentation directly.

    ::

        >>> import uqbar.apis
        >>> documenter = uqbar.apis.SummarizingModuleDocumenter(
        ...     'uqbar.io',
        ...     module_documenters=[
        ...         uqbar.apis.ModuleDocumenter('uqbar.io.Timer'),
        ...         ],
        ...     )
        >>> print(str(documenter))
        .. _uqbar--io:
        <BLANKLINE>
        io
        ==
        <BLANKLINE>
        .. automodule:: uqbar.io
        <BLANKLINE>
        .. currentmodule:: uqbar.io
        <BLANKLINE>
        .. container:: svg-container
        <BLANKLINE>
           .. inheritance-diagram:: uqbar
              :lineage: uqbar.io
        <BLANKLINE>
        .. raw:: html
        <BLANKLINE>
           <hr/>
        <BLANKLINE>
        .. rubric:: Classes
           :class: section-header
        <BLANKLINE>
        .. toctree::
           :hidden:
        <BLANKLINE>
           Timer
        <BLANKLINE>
        .. autosummary::
           :nosignatures:
        <BLANKLINE>
           ~Timer.Timer
        <BLANKLINE>
        .. raw:: html
        <BLANKLINE>
           <hr/>
        <BLANKLINE>
        .. rubric:: Functions
           :class: section-header
        <BLANKLINE>
        .. autosummary::
           :nosignatures:
        <BLANKLINE>
           ~find_common_prefix
           ~find_executable
           ~relative_to
           ~walk
           ~write
        <BLANKLINE>
        .. autofunction:: find_common_prefix
        <BLANKLINE>
        .. autofunction:: find_executable
        <BLANKLINE>
        .. autofunction:: relative_to
        <BLANKLINE>
        .. autofunction:: walk
        <BLANKLINE>
        .. autofunction:: write

    :param package_path: the module path of the module to document
    :param document_private_members: whether to documenter private module members
    :param member_documenter_classes: a list of
        :py:class:`~uqbar.apis.MemberDocumenter` subclasses, defining what classes
        to use to identify and document module members
    :param module_documenters: a list of of documenters for submodules and
        subpackages of the documented module; these are generated by an
        :py:class:`~uqbar.apis.APIBuilder` instance rather than the module
        documenter directly
    :param api_builder: an :py:class:`~uqbar.apis.APIBuilder` instance
    """

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Documenters'

    ### SPECIAL METHODS ###

    def __str__(self) -> str:
        result = self._build_preamble()
        package_path = self.package_path.partition('.')[0]
        lineage_path = self.package_path
        result.extend([
            '',
            '.. container:: svg-container',
            '',
            '   .. inheritance-diagram:: {}'.format(package_path),
            '      :lineage: {}'.format(lineage_path),
            ])
        if self.is_nominative:
            result.extend(['', str(self.member_documenters[0])])
        else:
            if self.is_package:
                subpackage_documenters = [
                    _ for _ in self.module_documenters or []
                    if _.is_package or not _.is_nominative
                    ]
                if subpackage_documenters:
                    result.extend([
                        '',
                        '.. raw:: html',
                        '',
                        '   <hr/>',
                        '',
                        '.. rubric:: Subpackages',
                        '   :class: section-header',
                        ])
                    result.extend(self._build_toc(
                        subpackage_documenters,
                        show_full_paths=True,
                        ))
            for section, documenters in self.member_documenters_by_section:
                result.extend([
                    '',
                    '.. raw:: html',
                    '',
                    '   <hr/>',
                    '',
                    '.. rubric:: {}'.format(section),
                    '   :class: section-header',
                    ])
                local_documenters = [
                    documenter for documenter in documenters
                    if documenter.client.__module__ == self.package_path
                    ]
                result.extend(self._build_toc(documenters))
                for local_documenter in local_documenters:
                    result.extend(['', str(local_documenter)])
        return '\n'.join(result)

    ### PRIVATE METHODS ###

    def _build_toc(
        self,
        documenters,
        show_full_paths: bool=False,
        **kwargs
    ) -> List[str]:
        result: List[str] = []
        if not documenters:
            return result
        toctree_paths = set()
        for documenter in documenters:
            path = self._build_toc_path(documenter)
            if path:
                toctree_paths.add(path)
        if toctree_paths:
            result.extend(['', '.. toctree::', '   :hidden:', ''])
            for toctree_path in sorted(toctree_paths):
                result.append('   {}'.format(toctree_path))
        result.extend([
            '',
            '.. autosummary::',
            '   :nosignatures:',
            '',
            ])
        for documenter in documenters:
            template = '   ~{}'
            if show_full_paths:
                template = '   {}'
            path = documenter.package_path.rpartition(
                self.package_path + '.')[-1]
            result.append(template.format(path))
        return result

    ### PUBLIC PROPERTIES ###

    @property
    def member_documenters_by_section(self) -> List[Tuple[str, List[MemberDocumenter]]]:
        result: MutableMapping[str, List[MemberDocumenter]] = {}
        for documenter in self.member_documenters:
            result.setdefault(
                documenter.documentation_section, []).append(documenter)
        for module_documenter in self.module_documenters or []:
            if not module_documenter.is_nominative:
                continue
            documenter = module_documenter.member_documenters[0]
            result.setdefault(
                documenter.documentation_section, []).append(documenter)
        return sorted(result.items())
