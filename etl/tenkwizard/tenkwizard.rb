#!/usr/bin/ruby

require 'rubygems'
require 'mechanize'

class TenKWizard

  USER_AGENT = 'Mac FireFox'
  LOGIN = 'jmorris@sunlightfoundation.com'
  PASSWORD = 'jmorris'
  COOKIE_FILE = 'cookies.yaml'
  MAIN_10K_URL = 'http://www.10kwizard.com/main.php'
  
  attr_accessor :agent, :current_page

  def initialize(load_cookies = true)
    @agent = WWW::Mechanize.new
    @agent.user_agent_alias = USER_AGENT    
    @current_page = nil

    @agent.cookie_jar.load(COOKIE_FILE) if load_cookies
  end

  def load_main_page()
    @agent.get(MAIN_10K_URL) do |page|
      @current_page = page
    end
  end

  def login(dump_cookies = true)
    @agent.cookie_jar.clear!
    
    @agent.get(MAIN_10K_URL) do |page|
      login_form = page.forms[0]
      login_form.email = LOGIN
      login_form.password = PASSWORD
      sleep 1
      page = login_form.submit
      # now follow the meta redirects
      @current_page = self._follow_meta(@agent, page)
    end
    
    @agent.cookie_jar.save_as(COOKIE_FILE) if dump_cookies       
  end  

  def _follow_meta(p)
    found_meta = false
    
    p.search("//meta[@http-equiv='refresh']").each do |meta|
      if meta.attributes['http-equiv'].to_s=='refresh' then
         found_meta = true
         p = @agent.get meta.attributes['href'].to_s.gsub(/'/,'')
      end
    end
  
    p = follow_meta(p) if p.search("//meta[@http-equiv='refresh']").length>0 and found_meta
      
    return p
  end
  
  def get_compensation_data(ticker_symbol)
    load_main_page()
    sleep 1
    
    form = @current_page.forms[1]
    form.sym = ticker_symbol
    form['fg[]'] = '22'
    @current_page = form.submit
    sleep 1
    
    @current_page.search('a[@onclick]').each do |link|
      if link.inner_html=~/compensation table/i then
        puts link.attributes['onclick']
      end
    end
    
    #@curent_page.search("#results table tr td.txt a[@title='Download spreadsheets']").each do |link|
    #@agent.get link.attributes['href'].to_s

      
    #end
    
    
    
    
  end

end
