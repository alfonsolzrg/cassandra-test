var questionnaire = new Vue({
  delimiters: ['<%', '%>'],
  el: '#questionnaire',
  data: {
    name: '',
    vim_emacs: '',
    ide_texteditor: '',
    compiled_interpreted: '',
    favorite_ide: '',
    marry: '',
    kiss: '',
    kill: '',
    java_net: '',
    cloud_providers: '',
    team_size: '',
    preferred_location: '',
  },
  methods: {
    track: function(element) {
      console.log('Element '+element+' has changed! New value: '+this[element]);
      $.post('/feed', {
        element_name: element,
        element_value: this[element]
      });
    }
  }
});