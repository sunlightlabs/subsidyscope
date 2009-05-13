require 'yaml'
data_in = YAML::load_file 'starter_glossary.yaml'

data_out = []

data_in.each do |item|
  term       = item['fields']['term']
  slug       = item['fields']['slug']
  definition = item['fields']['definition']

  data_out << {
    :term       => term,
    :slug       => slug,
    :definition => definition
  }
end

puts YAML::dump(data_out)
