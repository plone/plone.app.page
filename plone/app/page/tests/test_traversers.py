import unittest2 as unittest

from plone.app.page.testing import PAGE_INTEGRATION_TESTING

class TestTraversers(unittest.TestCase):

    layer = PAGE_INTEGRATION_TESTING

    def test_page_layout_traverser_registered(self):
        from plone.resource.file import FilesystemFile
        portal = self.layer['portal']
        
        layout = portal.restrictedTraverse('++pagelayout++testlayout1/page.html')
        self.assertTrue(isinstance(layout, FilesystemFile))

    def test_page_layouts_vocabulary(self):
        from zope.schema.vocabulary import getVocabularyRegistry
        portal = self.layer['portal']
        
        vocab = getVocabularyRegistry().get(portal, 'plone.availablePageLayouts')
        vocab = list(vocab)
        vocab.sort(key=lambda t: t.token)
        
        self.assertEqual(len(vocab), 2)
        
        self.assertEqual(vocab[0].token, 'testlayout1')
        self.assertEqual(vocab[0].title, 'Testlayout1')
        self.assertEqual(vocab[0].value, u'/++pagelayout++testlayout1/page.html')
        
        self.assertEqual(vocab[1].token, 'testlayout2')
        self.assertEqual(vocab[1].title, 'My page layout')
        self.assertEqual(vocab[1].value, u'/++pagelayout++testlayout2/mypage.html')
